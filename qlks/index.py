from qlks import login, utils, models
from qlks.admin import *
from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user, logout_user
import cloudinary.uploader


@app.route("/")
def home():
    room_type = utils.get_all_room_type()

    return render_template("index.html", room_type=room_type)


@app.route('/api/find-room', methods=['post'])
def find_room():
    data = request.json

    if data:
        price = data.get('price')
        floor = data.get('floor')

        if price or floor:
            jrooms = utils.find_room(price, floor)
            return jsonify(jrooms)
        else:
            jrooms = utils.get_all_room()
            return jsonify(jrooms)
    #     find = session.get('find')
    #     if not find:
    #         find = {}
    #
    #     if rooms in find:
    #         pass
    #     else:
    #         find[rooms] = {"rooms": rooms}
    #
    # session['find'] = find


@app.route('/api/find-room/booked', methods=['post'])
def find_room_booked():
    data = request.json

    if data:
        price = data.get('price')
        floor = data.get('floor')

        if price or floor:
            jrooms = utils.find_room(price, floor, booked=True)
            return jsonify(jrooms)
        else:
            jrooms = utils.get_all_room()
            return jsonify(jrooms)


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_user", methods=["post"])
def log_user_in():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username, password)

    if user:
        login_user(user=user)
        if user.user_role_id == 1:
            return redirect("/admin")

    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/signup", methods=['get', 'post'])
def sign_up():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        pwd_check = request.form.get('pwd_check')
        ava_path = None

        try:
            if password.strip().__eq__(pwd_check.strip()) and utils.check_username(username) is None:
                avatar = request.files.get('avatar')
                if avatar:
                    respond = cloudinary.uploader.upload(avatar)
                    ava_path = respond['secure_url']
                utils.add_user(name, username, password, email, avatar=ava_path)
                return redirect("/")
            else:
                err_msg = "Wrong password!!!!"
        except Exception as ex:
            err_msg = "System went wrong: " + str(ex)

    return render_template("signup.html", err_msg=err_msg)


@app.route("/book_room", methods=['post', 'get'])
def book_room():
    form = request.form
    if form:
        date_rent = form.get('date-rent')
        date_end = form.get('date-end')
        number_of_people = form.get('number-of-people')
        foreign = form.get('foreign')
        customer_id = form.get('customer-id')
        customer_name = form.get('customer-name')
        room_id = form.get('room-id')
        result = utils.add_book_info(room_id, date_rent, date_end,
                                     number_of_people, foreign, customer_id, customer_name)
        if result.__eq__("True"):
            utils.change_booked_status(room_id)

        return render_template('book.html', dr=date_rent, de=date_end, n=number_of_people, f=foreign, ci=customer_id,
                               cn=customer_name, ri=room_id, result=result)
    else:
        return render_template('book.html')


@app.route("/rent_room", methods=['post', 'get'])
def rent_room():
    form = request.form
    if form:
        date_rent = form.get('date-rent-2')
        date_end = form.get('date-end-2')
        number_of_people = form.get('number-of-people-2')
        foreign = form.get('foreign-2')
        customer_id = form.get('customer-id-2')
        customer_name = form.get('customer-name-2')
        room_id = form.get('room-id-2')
        result = utils.add_rent_info(room_id, date_rent, date_end,
                                     number_of_people, foreign, customer_id, customer_name)
        if result.__eq__("True"):
            utils.change_rented_status(room_id)

        return render_template('rent.html', dr=date_rent, de=date_end, n=number_of_people, f=foreign, ci=customer_id,
                               cn=customer_name, ri=room_id, result=result)
    else:
        return render_template('rent.html')


@app.route('/api/auto_write/', methods=['post'])
def auto_write():
    data = request.json

    if data:
        id = data.get('id')
        return jsonify(utils.get_book_info(id))


@app.route("/payment", methods=['post', 'get'])
def payment():
    id = request.form.get('idcustomer')
    return render_template('payment.html', find_rent=utils.find_rent(id), rooms=utils.rent_room_list(id),
                            add=utils.add_receipt(id), addDetail=utils.add_receipt_detail(id), pay=utils.pay(id),
                            change=utils.change_rent(id))


if __name__ == "__main__":
    app.run(debug=True)
