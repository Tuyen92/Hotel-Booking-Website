from qlks import db
from sqlalchemy import Column, Integer, Float, String, BOOLEAN, DATETIME, ForeignKey, DATE, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    avatar = Column(String(100))
    active = Column(BOOLEAN, default=True)
    created_date = Column(DATETIME, default=datetime.now())
    user_role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False, default=3)


class UserRoles(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False)
    users = relationship('User', backref='user_role', lazy=True)

    def __str__(self):
        return self.role


class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(100), nullable=False)
    detail_id = Column(Integer, ForeignKey('room_detail.id'), nullable=False)
    rented = Column(BOOLEAN, default=False)
    rent_info = relationship('RentInfo', backref='room', lazy=True)
    booked = Column(BOOLEAN, default=False)
    book_info = relationship('BookInfo', backref='room', lazy=True)
    floor = Column(Integer, nullable=False)
    receipt_detail = relationship('ReceiptDetails', backref='room', lazy=True)


class RoomDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    number_of_bed = Column(Integer, nullable=False)
    rooms = relationship('Room', backref='room_detail', lazy=False)
    type_id = Column(Integer, ForeignKey('room_type.id'), nullable=False)

    def __str__(self):
        return str(self.id)


class RoomType(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20), nullable=False)
    description = Column(String(100))
    rooms_detail = relationship('RoomDetail', backref='room_type', lazy=False)

    def __str__(self):
        return self.type


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=True)
    name = Column(String(100), nullable=True)
    day = Column(DATETIME, nullable=True)
    detail = relationship('ReceiptDetails', backref='receipt', lazy=True)
    total = Column(Integer)


class ReceiptDetails(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, primary_key=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(Integer)


class BookInfo(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    date_book = Column(DATETIME, nullable=False, default=datetime.now())
    date_rent = Column(DATETIME, nullable=False)
    date_end = Column(DATETIME)
    number_of_people = Column(Integer, nullable=False)
    foreign = Column(Integer, default=0, nullable=False)
    customer_id = Column(Integer, nullable=False)
    customer_name = Column(String(50), nullable=False)


class RentInfo(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    customer_id = Column(Integer, nullable=False)
    customer_name = Column(String(50), nullable=False)
    number_of_people = Column(Integer, nullable=False)
    foreign = Column(Integer, default=0, nullable=False)
    date_rent = Column(DATETIME, nullable=False)
    date_end = Column(DATETIME)


class Regulations(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200), nullable=False)
    value = Column(Float)
    unit = Column(String(100))


if __name__ == "__main__":
    db.create_all()

    # ur1 = UserRoles(role="manager")
    # ur2 = UserRoles(role="employee")
    # ur3 = UserRoles(role="customer")
    #
    # u1 = User(name="Loi", username='Loi', password='123', email='loi@gmail.com', user_role_id=1)
    # u2 = User(name="Bui", username='Bui', password='456', email='bui@gmail.com', user_role_id=2)
    # u3 = User(name="Quang", username='Quang', password='789', email='quang@gmail.com', user_role_id=3)
    #
    # db.session.add(ur1)
    # db.session.add(ur2)
    # db.session.add(ur3)
    #
    # db.session.add(u1)
    # db.session.add(u2)
    # db.session.add(u3)
    #
    # rgl1 = Regulations(content="Single Room's price", value="200000", unit="VNĐ/day")
    # rgl2 = Regulations(content="Double Room's price", value="400000", unit="VNĐ/day")
    # rgl3 = Regulations(content="Room has 3 person, surcharge", value="0.25", unit="per room")
    # rgl4 = Regulations(content="Room has foreign, room rate multiplier", value="1.5", unit="per room ")
    # rgl5 = Regulations(content="Using drinks, surcharge", value="30000", unit="VNĐ/bottle,can")
    # rgl6 = Regulations(content="Using alcoholic drinks, surcharge", value="50000", unit="VNĐ/bottle,can")
    # rgl7 = Regulations(content="Using snacks, surcharge", value="50000", unit="VNĐ/pack")
    # rgl8 = Regulations(content="Breaking furniture, surcharge", value="300000", unit="VNĐ/object")
    # rgl9 = Regulations(content="Losing hotel's stuff, surcharge", value="100000", unit="VNĐ/object")
    # rgl10 = Regulations(content="Date of renting must be 28 days from date of booking")
    #
    # db.session.add(rgl1)
    # db.session.add(rgl2)
    # db.session.add(rgl3)
    # db.session.add(rgl4)
    # db.session.add(rgl5)
    # db.session.add(rgl6)
    # db.session.add(rgl7)
    # db.session.add(rgl8)
    # db.session.add(rgl9)
    #
    # rt1 = RoomType(id=1, type="Single", description="1 bed, 1 - 2 person")
    # rt2 = RoomType(id=2, type="Double", description="2 bed, 2 - 3 person")
    # rt3 = RoomType(id=3, type="VIP", description="1 bed, 1 - 2 person, nice view")
    # rt4 = RoomType(id=4, type="VVIP", description="2 bed, 2 - 3 person, nice view")
    #
    # db.session.add(rt1)
    # db.session.add(rt2)
    # db.session.add(rt3)
    # db.session.add(rt4)
    #
    # rd1 = RoomDetail(id=1, price="200000", number_of_bed=1, type_id=1)
    # rd2 = RoomDetail(id=2, price="400000", number_of_bed=2, type_id=2)
    # rd3 = RoomDetail(id=3, price="600000", number_of_bed=1, type_id=3)
    # rd4 = RoomDetail(id=4, price="1200000", number_of_bed=2, type_id=4)
    #
    # db.session.add(rd1)
    # db.session.add(rd2)
    # db.session.add(rd3)
    # db.session.add(rd4)
    #
    # r1 = Room(id=101, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=1)
    # r2 = Room(id=102, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=1)
    # r3 = Room(id=103, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=1)
    # r4 = Room(id=104, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=1)
    # r5 = Room(id=105, image="../static/imgs/vip.jpg", detail_id=3, rented=0, booked=0, floor=1)
    # r6 = Room(id=106, image="../static/imgs/vvip.jpg", detail_id=4, rented=0, booked=0, floor=1)
    # r7 = Room(id=201, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=2)
    # r8 = Room(id=202, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=2)
    # r9 = Room(id=203, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=2)
    # r10 = Room(id=204, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=2)
    # r11 = Room(id=205, image="../static/imgs/vip.jpg", detail_id=3, rented=0, booked=0, floor=2)
    # r12 = Room(id=206, image="../static/imgs/vvip.jpg", detail_id=4, rented=0, booked=0, floor=2)
    # r13 = Room(id=301, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=3)
    # r14 = Room(id=302, image="../static/imgs/single.jpg", detail_id=1, rented=0, booked=0, floor=3)
    # r15 = Room(id=303, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=3)
    # r16 = Room(id=304, image="../static/imgs/double.jpg", detail_id=2, rented=0, booked=0, floor=3)
    # r17 = Room(id=305, image="../static/imgs/vip.jpg", detail_id=3, rented=0, booked=0, floor=3)
    # r18 = Room(id=306, image="../static/imgs/vvip.jpg", detail_id=4, rented=0, booked=0, floor=3)
    #
    # db.session.add(r1)
    # db.session.add(r2)
    # db.session.add(r3)
    # db.session.add(r4)
    # db.session.add(r5)
    # db.session.add(r6)
    # db.session.add(r7)
    # db.session.add(r8)
    # db.session.add(r9)
    # db.session.add(r10)
    # db.session.add(r11)
    # db.session.add(r12)
    # db.session.add(r13)
    # db.session.add(r14)
    # db.session.add(r15)
    # db.session.add(r16)
    # db.session.add(r17)
    # db.session.add(r18)

    db.session.commit()
