from django.utils.timezone import now


class BodyClassMixin(object):
    body_classes = ()

    def get_body_classes(self):
        return self.body_classes

    def get_context_data(self, **kwargs):
        context = super(BodyClassMixin, self).get_context_data(**kwargs)
        context['body_classes'] = self.get_body_classes()

        return context


class MenuSelectionMixin(object):
    menu_selection = None

    def get_menu_selection(self):
        return self.menu_selection

    def get_context_data(self, **kwargs):
        context = super(MenuSelectionMixin, self).get_context_data(**kwargs)
        context['menu_selection'] = self.get_menu_selection()

        return context


class TitlePartsMixin(object):
    title_parts = []

    def get_title_parts(self):
        return self.title_parts

    def get_context_data(self, **kwargs):
        context = super(TitlePartsMixin, self).get_context_data(**kwargs)
        context['title_parts'] = self.get_title_parts()

        return context


class MetaKeywordsMixin(object):
    meta_keywords = []

    def get_meta_keywords(self):
        return self.meta_keywords

    def get_context_data(self, **kwargs):
        context = super(MetaKeywordsMixin, self).get_context_data(**kwargs)
        context['meta_keywords'] = self.get_meta_keywords()

        return context


class MetaDescriptionMixin(object):
    meta_description = u''

    def get_meta_description(self):
        return self.meta_description

    def get_context_data(self, **kwargs):
        context = super(MetaDescriptionMixin, self).get_context_data(**kwargs)
        context['meta_description'] = self.get_meta_description()

        return context


class MetaAuthorMixin(object):
    meta_author = u''

    def get_meta_author(self):
        return self.meta_author

    def get_context_data(self, **kwargs):
        context = super(MetaAuthorMixin, self).get_context_data(**kwargs)
        context['meta_author'] = self.get_meta_author()

        return context


class SocialGraphDataMixin(object):
    social_post_kind = 'article'
    social_image = None
    social_title = None
    social_description = None
    twitter_creator = None

    def get_social_post_kind(self):
        return self.social_post_kind

    def get_social_image(self):
        return self.social_image

    def get_social_title(self):
        return self.social_title

    def get_social_description(self):
        return self.social_description

    def get_twitter_creator(self):
        return self.twitter_creator

    def get_context_data(self, **kwargs):
        context = super(SocialGraphDataMixin, self).get_context_data(**kwargs)
        context['social_post_kind'] = self.get_social_post_kind()
        context['social_image'] = self.get_social_image()
        context['social_title'] = self.get_social_title()
        context['social_description'] = self.get_social_description()
        context['twitter_creator'] = self.get_twitter_creator()

        return context


class BootstrapMixin(
    BodyClassMixin, MenuSelectionMixin, TitlePartsMixin,
    MetaKeywordsMixin, MetaDescriptionMixin, MetaAuthorMixin,
    SocialGraphDataMixin
):
    pass
