import datetime

from sqlalchemy import func
from qlks.models import *
from sqlalchemy.sql import extract
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password.strip())).first()


def add_user(name, username, password, email, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    c1 = User(name=name, username=username, password=password, email=email, avatar=kwargs.get('avatar'))

    db.session.add(c1)

    db.session.commit()

    return True


def check_username(username):
    return User.query.filter(User.username.__eq__(username)).first()


def find_room(price=None, floor=None, booked=False):
    prooms = []
    jrooms = []
    if price:
        rooms = RoomDetail.query.filter(RoomDetail.price == price).all()
        for room in rooms:
            for r in room.rooms:
                if r.booked.__eq__(booked) and r.rented.__eq__(False):
                    prooms.append(r.id)
    if floor:
        rooms = Room.query.filter(Room.floor.__eq__(floor)).all()
        if prooms.__len__() != 0:
            for room in rooms:
                if room.floor.__eq__(floor) and room.id in prooms:
                    jrooms.append(room.id)
        else:
            for room in rooms:
                if room.floor.__eq__(floor):
                    jrooms.append(room.id)
    else:
        jrooms = prooms
    return jrooms


def get_all_room():
    jrooms = []
    rooms = Room.query.all()
    for room in rooms:
        jrooms.append(room.id)
    return jrooms


def get_all_room_type():
    jrooms_type = []
    rooms_type = RoomType.query.all()

    for r in rooms_type:
        price = get_room_price(r.id)
        img = get_room_image(r.id)
        jrooms_type.append({'type': r.type, 'des': r.description, 'price': price, 'img':img})

    return jrooms_type


def get_room_price(id):
    price = 10000
    room_price = RoomDetail.query.filter(RoomDetail.type_id.__eq__(id)).all()
    for rp in room_price:
        if rp.price > price:
            price = rp.price
    return price


def get_room_image(id):
    room_img = RoomDetail.query.filter(RoomDetail.type_id.__eq__(id)).first()
    return room_img.rooms[0].image


def add_book_info(room_id, date_rent, date_end, number_of_people, foreign, customer_id, customer_name):
    b1 = BookInfo(room_id=room_id, date_rent=date_rent, date_end=date_end, number_of_people=number_of_people,
                  foreign=foreign, customer_id=customer_id, customer_name=customer_name)

    db.session.add(b1)

    db.session.commit()
    return True


def get_book_info(id):
    jbook_info = []

    book_info = Room.query.get(id).book_info[-1]
    jbook_info.append(book_info.date_rent.date())
    jbook_info.append(book_info.date_end.date())
    jbook_info.append(book_info.number_of_people)
    jbook_info.append(book_info.foreign)
    jbook_info.append(book_info.customer_id)
    jbook_info.append(book_info.customer_name)

    return jbook_info


def change_booked_status(room_id):
    room = Room.query.filter(Room.id.__eq__(room_id)).first()
    room.booked = True

    db.session.commit()


def add_rent_info(room_id, date_rent, date_end, number_of_people, foreign, customer_id, customer_name):
    b1 = RentInfo(room_id=room_id, date_rent=date_rent, date_end=date_end, number_of_people=number_of_people,
                  foreign=foreign, customer_id=customer_id, customer_name=customer_name)

    db.session.add(b1)

    db.session.commit()
    return True


def change_rented_status(room_id):
    room = Room.query.filter(Room.id.__eq__(room_id)).first()
    if room.rented and room.rented.__eq__(True):
        room.rented = False
    else:
        room.rented = True

    db.session.commit()


def room_stats(kw=None, from_date=None, to_date=None):
    pr = db.session.query(Room.id,RoomDetail.id, RoomType.type, func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price)) \
        .outerjoin(Room, Room.detail_id.__eq__(RoomDetail.id)) \
        .outerjoin(ReceiptDetails, ReceiptDetails.room_id.__eq__(Room.id), isouter=False)\
        .outerjoin(Receipt, Receipt.id.__eq__(ReceiptDetails.receipt_id))\
        .outerjoin(RoomType, RoomType.id.__eq__(RoomDetail.type_id)).group_by(Room.detail_id)
    if kw:
        pr = pr.filter(RoomType.type.contains(kw))
    if from_date:
        pr = pr.filter(Receipt.day.__ge__(from_date))
    if to_date:
        pr = pr.filter(Receipt.day.__le__(to_date))

    return pr.all()


def rental_room():
    return RentInfo.query.with_entities(RentInfo.room_id, func.count(RentInfo.id)).group_by(RentInfo.room_id).all()


def room_month_stats(year):
    return db.session.query(extract('month', Receipt.day),\
           func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price)).join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
           .filter(extract('year', Receipt.day) == year).group_by(extract('month', Receipt.day))\
           .order_by(extract('month', Receipt.day)).all()


def find_rent(id=None):
    info = db.session.query(Room.id, RentInfo.customer_name, RentInfo.date_rent, RentInfo.date_end)\
        .outerjoin(RoomDetail, RoomDetail.id.__eq__(Room.detail_id))\
        .outerjoin(RentInfo, RentInfo.room_id.__eq__(Room.id)).filter(RentInfo.customer_id.__eq__(id)).group_by(RentInfo.customer_id).all()
    return info


def count(id):
    room_list = db.session.query(Room.id, RentInfo.number_of_people, RentInfo.foreign, RoomDetail.price) \
        .outerjoin(RoomDetail, RoomDetail.id.__eq__(Room.detail_id)) \
        .outerjoin(RentInfo, RentInfo.room_id.__eq__(Room.id)).filter(RentInfo.customer_id.__eq__(id)).all()
    return room_list


def pay(id):
    total = 0
    for c in count(id):
        if c[1] == 3:
            total = total+c[3]+(c[3]*0.25)
        if c[2] != 0:
            total = total+c[3]*1.5
        if c[1] != 3 and c[2] == 0:
            total = total + c[3]
    return total


def rent_room_list(id=None):
    rooms = db.session.query(Room.id, RoomDetail.price)\
        .outerjoin(RentInfo, RentInfo.room_id.__eq__(Room.id))\
        .outerjoin(RoomDetail, RoomDetail.id.__eq__(Room.detail_id))\
        .filter(RentInfo.customer_id.__eq__(id)).group_by(RentInfo.room_id).all()
    return rooms


def change_rent(id=None):
    for r in rent_room_list(id):
        change_rented_status(r[0])
    return True


def add_receipt(customer_id=None):
    name = " "
    day = datetime.now()
    if customer_id:
        for tt in find_rent(customer_id):
            name = tt[1]
            day = tt[3]
        r = Receipt(customer_id=customer_id, total=pay(customer_id), name=name, day=day)
        db.session.add(r)

        db.session.commit()
    return True


def add_receipt_detail(customer_id=None):
    receipt_id = db.session.query(Receipt.id).filter(Receipt.customer_id.__eq__(customer_id)).first()
    rooms = 0
    price = 0
    if customer_id:
        for rs in rent_room_list(customer_id):
            rooms = rs[0]
            price = rs[1]
            rd = ReceiptDetails(receipt_id=receipt_id[0], room_id=rooms, unit_price=price)
            db.session.add(rd)
        db.session.commit()
    return True