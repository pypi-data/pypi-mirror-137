import random
import string
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from djangoldp.models import Model
from .permissions import CirclePermissions, CircleMemberPermissions
from .views import CircleMembersViewset
import logging

logger = logging.getLogger('djangoldp')


MODEL_MODIFICATION_USER_FIELD = 'modification_user'
STATUS_CHOICES = [
    ('Public', 'Public'),
    ('Private', 'Private'),
    ('Archived', 'Archived'),
]

circle_fields = ["@id", "name", "subtitle", "description", "creationDate", "status", "owner", "jabberID", "jabberRoom", "members", "parentCircle", "children"]
if 'djangoldp_community' in settings.DJANGOLDP_PACKAGES:
    circle_fields += ['community']

if 'djangoldp_polls' in settings.DJANGOLDP_PACKAGES:
    circle_fields += ['polls']

if 'djangoldp_resource' in settings.DJANGOLDP_PACKAGES:
    circle_fields += ['resources']

if 'djangoldp_event' in settings.DJANGOLDP_PACKAGES:
    circle_fields += ['events']


class Circle(Model):
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    subtitle = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    creationDate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Public')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_circles", on_delete=models.SET_NULL,
                              null=True, blank=True)
    parentCircle = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                                     help_text="A circle can optionally be nested within a parent")
    jabberID = models.CharField(max_length=255, blank=True, null=True, unique=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta(Model.Meta):
        empty_containers = ["owner"]
        auto_author = 'owner'
#        depth = 1 # Disabled due to owner being serialized
        permission_classes = [CirclePermissions]
        anonymous_perms = []
        authenticated_perms = []
        owner_perms = []
        serializer_fields = circle_fields
        rdf_type = 'hd:circle'

    def __str__(self):
        try:
            return '{} ({})'.format(self.name, self.urlid)
        except:
            return self.urlid

    def get_admins(self):
        return self.members.filter(is_admin=True)


class CircleMember(Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="circles", null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        try:
            return '{} -> {} ({})'.format(self.circle.urlid, self.user.urlid, self.urlid)
        except:
            return self.urlid

    class Meta(Model.Meta):
        container_path = "circle-members/"
        permission_classes = [CircleMemberPermissions]
        anonymous_perms = []
        authenticated_perms = ['view', 'add']
        owner_perms = ['inherit']
        unique_together = ['user', 'circle']
        rdf_type = 'hd:circlemember'
        view_set = CircleMembersViewset

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.username == "hubl-workaround-493":
                self.user = None
        # cannot be duplicated CircleMembers
        if not self.pk and CircleMember.objects.filter(circle=self.circle, user=self.user).exists():
            return

        super(CircleMember, self).save(*args, **kwargs)

@receiver(post_save, sender=CircleMember)
def fix_user_hubl_workaround_493(sender, instance, **kwargs):
    if not instance.user:
        try:
            request_user = getattr(instance, MODEL_MODIFICATION_USER_FIELD, None)
            if request_user is None:
                raise Exception('request user was unexpectedly None!')
            user = get_user_model().objects.get(pk=request_user.pk)
            instance.user = user
            instance.save()
        except Exception as e:
            logger.error('error in Circle.fix_user_hubl_workaround_493.. ' + str(e))
            if instance.pk is not None:
                instance.delete()

@receiver(pre_save, sender=Circle)
def set_jabberid(sender, instance, **kwargs):
    if getattr(settings, 'JABBER_DEFAULT_HOST', False) and not instance.jabberID:
        instance.jabberID = '{}@conference.{}'.format(
            ''.join(
                [
                    random.choice(string.ascii_letters + string.digits)
                    for n in range(12)
                ]
            ).lower(),
            settings.JABBER_DEFAULT_HOST
        )
        instance.jabberRoom = True

@receiver(post_save, sender=Circle)
def set_owner_as_member(instance, created, **kwargs):
    # add owner as an admin member
    if instance.owner is not None:
        try:
            owner_member = instance.members.get(user=instance.owner)
            if not owner_member.is_admin:
                owner_member.is_admin = True
                owner_member.save()
        except CircleMember.DoesNotExist:
            CircleMember.objects.create(user=instance.owner, circle=instance, is_admin=True)

@receiver(post_delete, sender=CircleMember)
def delete_circle_on_last_member_delete(sender, instance, **kwargs):
    # if this was the last member of the circle, the circle should be deleted too
    if instance.circle.pk is not None and instance.circle.members.count() == 0:
        instance.circle.delete()

@receiver(pre_delete, sender=CircleMember)
def manage_deleted_owner(sender, instance, **kwargs):
    # was the owner removed?
    if instance.user is not None and instance.user == instance.circle.owner:
        # if there are another admin: pick one, set them as owner
        alt = instance.circle.members.filter(is_admin=True).exclude(user=instance.user)[:1]
        if not alt.exists():
            # if there is another member: pick one, set them as owner
            alt = instance.circle.members.all().exclude(user=instance.user)[:1]
        if alt.exists():
            instance.circle.owner = alt[0].user
            instance.circle.save()
