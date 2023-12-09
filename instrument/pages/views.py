from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    """Отображение страницы О нас."""

    template_name = 'pages/about.html'


class BuyersTemplateView(TemplateView):
    """Отображение страницы Покупателям."""

    template_name = 'pages/buyers.html'


class ContactsTemplateView(TemplateView):
    """Отображение страницы Контакты."""

    template_name = 'pages/contacts.html'
