class PageTitleViewMixin:
    title = ""

    def get_title(self):
        return self.title
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context["title"] = title
        return context