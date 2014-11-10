from DB import *
from flask import json
import requests
import appconfig
import datetime

class model:

    def __init__(self):
        self.cryptkey = appconfig.CRYPT_KEY

    def check_user(self, email, password):
        db = DB()
        sql = '''SELECT
                      u.email as email,
                      c.name as name,
                      c.address as address,
                      c.city as city,
                      c.state as state,
                      c.zip as zip,
                      c.apt_number as apartment,
                      u.password as password,
                      c.rememberme as  rememberme,
                      c.repeat_option as repeat_option,
                      c.phone as phone,
                      c.id as customer_id
                      FROM users u
                        LEFT JOIN customers c on u.id=c.user WHERE u.email=%s AND u.password=%s '''


        query = db.query(sql, (email, password, ))
        user = query.fetchone()
        db.close()
        if user:
            return self.format_result([user], 1, 'User found')
        return self.format_result({}, '0', 'User not found')

    def password_reset(self, email):
        db = DB()
        sql = '''SELECT email FROM users u WHERE u.email=%s '''
        query = db.query(sql, (email, ))
        user = query.fetchone()
        if user:

            if appconfig.ip == '127.0.0.1':
                url = 'http://snazzy.lcl/ajax/reset_password'
            else:
                url = 'http://188.2.16.19/snazzy.local/ajax/reset_password'

            data = {'email': email}
            requests.post(url, data=data)

            return self.format_result([email], 1, 'Email sent to user')

        db.close()
        return False

    def privacy(self):
        url = 'http://188.2.16.19/snazzy.local/staticios/privacy.html'
        params = {}
        r = requests.get(url, params=params)
        return self.format_result([{"result":r.content}], 1, "Privacy")

    def legal(self):
       url = 'http://188.2.16.19/snazzy.local/staticios/legal.html'
       params = {}
       r = requests.get(url, params=params)
       return self.format_result([{"result":r.content}], 1, "Legal")

    def about(self):
        url = 'http://188.2.16.19/snazzy.local/staticios/about.html'
        params = {}
        r = requests.get(url, params=params)
        return self.format_result([{"result":r.content}], 1, 'About us')

    def prices(self):
        db = DB()
        sql = '''SELECT price, description FROM item_types '''
        query = db.query(sql)
        prices = query.fetchall()
        db.close()
        return self.format_result(prices, 1, "Prices list")

    def howitworks(self):
        url = 'http://188.2.16.19/snazzy.local/staticios/howitworks.html'
        params = {}
        r = requests.get(url, params=params)
        return self.format_result([{"result":r.content}], 1, 'How it works')
    
    def format_result(self, result, status, message):
        response = {'response': result, 'status': status, 'message': message}
        return json.jsonify(response)

    def check_fornew_user(self, email):
        db = DB()
        sql = '''SELECT id FROM users WHERE email=%s '''
        query = db.query(sql, (email,))
        users = query.fetchall()
        db.close()
        if users:
            return self.format_result([email], 0, 'Email in use')
        return self.format_result([email], 0, 'Email not in use')

    def save_repeat_option(self, email, repeat_option):
        db = DB()
        sql = '''SELECT u.id as uid, c.id as cid FROM users u LEFT JOIN customers c on u.id=c.user WHERE email=%s '''
        query = db.query(sql, (email,))
        user = query.fetchone()

        if (user != None):

            sql = '''DELETE FROM customer_reminders WHERE customer=%s '''
            db.query(sql, (user['cid'],))
            db.conn.commit()

            if (repeat_option == 'Cancel'):

                sql = '''UPDATE customers SET repeat_option='' WHERE id=%s '''
                db.query(sql, (user['cid'],))
                db.conn.commit()

            else:
                now = datetime.datetime.today()

                if(repeat_option == 'Every week'):
                    repeaton = now + datetime.timedelta(days=6)
                elif(repeat_option == 'Every second week'):
                    repeaton = now + datetime.timedelta(days=13)
                else:
                    repeaton = now + datetime.timedelta(days=29)

                sql = '''INSERT INTO customer_reminders (customer, date_time) VALUES (%s, %s) '''
                db.query(sql, (user['cid'], repeaton, ))
                db.conn.commit()

                sql = '''UPDATE customers SET repeat_option=%s WHERE id=%s '''
                db.query(sql, (repeat_option, user['cid'],))
                db.conn.commit()

            return self.format_result([email], 1, "Status set.")
        db.close()
        return False

    def update_customer_info(self, name, address, city, zip_code, phone, apt_number, email, state):
        db = DB()
        sql = '''SELECT u.id as uid, c.id as cid FROM users u LEFT JOIN customers c on u.id=c.user WHERE email=%s '''
        query = db.query(sql, (email,))
        user = query.fetchone()
        if (user != None):

            sql = '''UPDATE customers SET name=%s, address=%s, city=%s, zip=%s, phone=%s, apt_number=%s, state=%s WHERE id=%s'''
            db.query(sql, (name, address, city, zip_code, phone, apt_number, state, user['cid'], ))
            db.conn.commit()
            db.close()
            return self.format_result([email], 1, "Data updated.")
        return False

    def customer_change_password(self, email, new_password, old_password):
        db = DB()
        sql = '''SELECT u.id as uid, c.id as cid FROM users u
                      LEFT JOIN customers c on u.id=c.user
                      WHERE u.email=%s AND u.password=%s '''

        query = db.query(sql, (email, old_password, ))
        user = query.fetchone()
        if (user != None):
            sql = '''UPDATE users SET password=%s WHERE email=%s '''
            db.query(sql, (new_password, email,))
            db.conn.commit()
            db.close()

            return self.format_result([email], 1, "New password is set.")

        return False

    #http://188.2.16.19/snazzy.local/ajax/get_times/los%20angeles/2014-05-27/pickup/false
    def get_pickup_times(self, pickup_date, city):

        url_times = 'http://188.2.16.19/snazzy.local/ajax/get_times/'+city+'/'+pickup_date+'/false'
        times = requests.get(url_times)

        return self.format_result(times.json(), 1, "Pickup times")

    #http://188.2.16.19/snazzy.local/ajax/get_dates/los%20angeles/2014-05-26/true/false/11
    def get_delivery_dates(self, city, pickup_date, start_hour):
        url_dates = 'http://188.2.16.19/snazzy.local/ajax/get_dates/'+city+'/'+pickup_date+'/true/false/'+start_hour
        dates = requests.get(url_dates)

        a = dates.json()

        if(a[0]['display'].find('div')):
            a[0]['display'] = a[0]['day'] + ", "+a[0]['month']+" "+a[0]['date']+" rush"

        return self.format_result(a, 1, "Delivery dates")

    #http://188.2.16.19/snazzy.local/ajax/get_times/los%20angeles/2014-05-27/delivery/true/2014-05-26_11
    def get_delivery_times(self, rush, city, delivery_date, pickup_date, start_hour):
        url_times = 'http://188.2.16.19/snazzy.local/ajax/get_times/'+city+'/'+delivery_date+'/delivery/'+rush+'/'+pickup_date+'_'+start_hour
        times = requests.get(url_times)



        return self.format_result(times.json(), 1, "Delivery times")

    def definedCititesForPrices(self):
        db = DB()
        sql = '''SELECT c.name as city FROM cities c'''
        query = db.query(sql)
        cities = query.fetchall()

        if(cities):
            return self.format_result(cities, 1, "Cities for prices.")
        return False

    def pricesForCity(self, city):
        db = DB()
        sql = '''SELECT it.id as id, it.description as descr, cp.price as price FROM city_items_prices cp
                        LEFT JOIN cities ci on cp.city=ci.id
                        LEFT JOIN item_types it on cp.item=it.id
                        WHERE ci.name=%s'''

        query = db.query(sql, (city,))
        prices = query.fetchall()
        sql = '''SELECT it.id as id, it.description as descr, it.price as price from item_types it'''
        query = db.query(sql)
        all_prices = query.fetchall()
        if(prices):
            for price in prices:
               for n,aprice in enumerate(all_prices):
                   if aprice['id'] == price['id']:
                       all_prices[n]['price'] = price['price']
                       print all_prices[n]['price']
        db.close()
        return self.format_result(all_prices, 1, "City %s item prices" % city)

    def gettestimonials(self):
        db = DB()
        sql = '''SELECT name, photo, text FROM testimonials'''
        query = db.query(sql)
        testimonials = query.fetchall()
        if(testimonials):
            return self.format_result(testimonials, 1, "All testimonials")
        return False

    def checkzip(self, zipcode):
        db = DB()
        sql = '''SELECT z.zip as zip, ci.name as city, s.name as state_name FROM allowed_zips z
                      LEFT JOIN cities ci ON z.city=ci.id
                      LEFT JOIN states s ON ci.state = s.id
                      WHERE z.zip=%s  '''
        query = db.query(sql, (zipcode,))
        zipdata = query.fetchone()
        if(zipdata):
            return self.format_result(zipdata, 1,  "Data for zip %s" %zipcode)
        return False

    def getstartdates(self, city):

        url_dates = 'http://188.2.16.19/snazzy.local/ajax/get_dates/'+city+'/today/false/false'

        dates = requests.get(url_dates)
        return self.format_result(dates.json(), 1, "Pickup dates")

    def getUserOrders(self, email):
        db = DB()
        sql = '''SELECT o.cryptic_id as order_id, s.name as status, p.activity_date as pickup, d.activity_date as delivery FROM orders o
                      LEFT JOIN customers c on o.customer=c.id
                      LEFT JOIN users u on u.id=c.user
                      LEFT JOIN status s on o.order_status=s.id
                      LEFT JOIN calendar p on o.pickup = p.id
                      LEFT JOIN calendar d on  o.deliver=d.id
                      WHERE u.email=%s'''
        query = db.query(sql, (email,))

        data = query.fetchall()
        if(data):
            return self.format_result(data, 1,  "Data for user %s" %email)
        return  False

    def getUserOrder(self, email, order_id):
        db = DB()
        sql = '''SELECT o.cryptic_id as order_id, p.activity_date as pickup, d.activity_date as delivery, o.special_instructions as special_instructions, o.special_driver_instructions as special_driver_instructions FROM orders o
                      LEFT JOIN customers c on o.customer=c.id
                      LEFT JOIN users u on u.id=c.user

                      LEFT JOIN calendar p on o.pickup = p.id
                      LEFT JOIN calendar d on  o.deliver=d.id
                      WHERE u.email=%s and o.cryptic_id=%s'''
        query = db.query(sql, (email, order_id, ))

        data = query.fetchall()
        if(data):
            return self.format_result(data, 1,  "Order Data for user %s and order id %s" % (email, order_id))
        return False

    def teststripe(self, cc, ccsecurity, ccexpm, ccexpy):

        import stripe

        stripe.api_key = "sk_test_ylGnsy8Yz09Pzv7nRRRsRsl7"
        token = stripe.Token.create(card={"number":cc, "exp_month": ccexpm, "exp_year": ccexpy, "cvc": ccsecurity},)
        return self.format_result(token, 1,  "Stripe token is")

    def createcustomer(self, email, password, address, city, name, phone, state, zip_code, facebook, google, apt_number):
        data_customer = {
                'email':email,
                'password':password,
                'address':address,
                'city':city,
                'name':name,
                'phone':phone,
                'state':state,
                'zip':zip_code,
                'facebook':facebook,
                'google':google,
                'apt_number':apt_number,
                'api':1
        }

        url = 'http://188.2.16.19/snazzy.local/ajax/register_customer'
        response = requests.post(url, data=data_customer)

        return response.json()

