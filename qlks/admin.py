from flask_admin import Admin
from qlks import app, db, utils
from qlks.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime

admin = Admin(app=app, name='Hotel Staff', template_mode='bootstrap4')


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date= request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',

                           rental_room=utils.rental_room(),
                           stats=utils.room_stats(kw=kw, from_date=from_date, to_date=to_date),
                           month_stats=utils.room_month_stats(year))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role_id == 1


class ManagerView(ModelView):
    can_view_details = True
    can_export = True
    edit_modal = True
    create_modal = True

    def is_accessible(self):
        return current_user.user_role_id == 1


class StaffView(ModelView):
    can_view_details = True
    can_edit = False
    can_delete = False
    can_export = True
    create_modal = True

    def is_accessible(self):
        return current_user.user_role_id == 2 or current_user.user_role_id == 1


class UserView(ManagerView):
    column_exclude_list = ['password', 'avatar']
    column_filters = ["name", "user_role"]
    column_sortable_list = ['name']
    column_searchable_list = ['name']
    form_excluded_columns = ['created_date', 'active']


class RoomView(ManagerView):
    column_exclude_list = ['image']
    column_filters = ["rented", "booked", "floor", "room_detail"]
    form_excluded_columns = ['rent_info', 'book_info', 'receipt', 'rented', 'booked']
    column_default_sort = [('rented', False), ('booked', False)]
    column_display_pk = True


class RoomDetailView(ManagerView):
    column_filters = ["price", "number_of_bed", "room_type"]
    form_excluded_columns = ['rooms']


class ReceiptView(StaffView):
    column_filters = ["name", "day"]


class RegulationView(ManagerView):
    column_filters = ["content"]


class BookView(ManagerView):
    column_filters = ['date_rent', 'date_end', 'customer_id', 'room']
    form_excluded_columns = ['date_book']


class RentView(ManagerView):
    column_filters = ['date_rent', 'date_end', 'customer_id', 'room']


admin.add_view(UserView(User, db.session, name="Users"))
admin.add_view(RoomView(Room, db.session, name="Rooms"))
admin.add_view(RoomDetailView(RoomDetail, db.session))
admin.add_view(ReceiptView(Receipt, db.session, name="Receipts"))
admin.add_view(RentView(RentInfo, db.session))
admin.add_view(BookView(BookInfo, db.session))
admin.add_view(ManagerView(Regulations, db.session))
admin.add_view(StatsView(name="Stats"))
admin.add_view(LogoutView(name="Logout"))