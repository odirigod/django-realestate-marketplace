from django.http import Http404

from homelink.mixins import LoginRequiredMixin


class ProductOwnerMixin(LoginRequiredMixin, object):
	def get_object(self, *args, **kwargs):
		user = self.request.user.profile
		obj = super().get_object(*args, **kwargs)
		if obj.realtor == user:
			return obj
		else:
			raise Http404