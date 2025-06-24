from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ad, AdImage, Favorite, Message
from .forms import AdForm, AdImageForm, MessageForm


# === Ad Views ===
class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ad_list')


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ad_list')


# === AdImage View ===
class AdImageCreateView(CreateView):
    model = AdImage
    form_class = AdImageForm
    template_name = 'ads/adimage_form.html'

    def form_valid(self, form):
        form.instance.ad_id = self.kwargs['ad_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ad_detail', kwargs={'pk': self.object.ad.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_id'] = self.kwargs['ad_id']
        return context



# === Favorite Views ===
class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'ads/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteCreateView(LoginRequiredMixin, CreateView):
    model = Favorite
    fields = ['ad']
    template_name = 'ads/favorite_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FavoriteDeleteView(LoginRequiredMixin, DeleteView):
    model = Favorite
    template_name = 'ads/favorite_confirm_delete.html'
    success_url = reverse_lazy('ad_list')

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


# === Message Views ===
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'ads/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'ads/message_form.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
