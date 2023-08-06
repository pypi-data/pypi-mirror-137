from flask_admin.contrib import sqla


class RedemptionModelView(sqla.ModelView):
    can_delete = False
    can_create = False
    column_list = ['command', 'title', 'enabled']
    column_editable_list = ['command', ]
    list_template = 'redemptions.html'

    def on_form_prefill(self, form, id):
        form.enabled.render_kw = {'readonly': True}
