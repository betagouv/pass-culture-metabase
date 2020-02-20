from db import SESSION


def create_user(id=1, email='test@email.com', can_book_free_offers=True, is_admin=False, postal_code='93100',
                departement_code='93', public_name='Test', date_created='2018-11-20',
                needs_to_fill_cultural_survey=True, cultural_survey_filled_date=None):
    if not cultural_survey_filled_date:
        cultural_survey_filled_date = 'NULL'
    else:
        cultural_survey_filled_date = f"'{cultural_survey_filled_date}'"
    password = '\x2432622431322445425a572e6d484754383242375558366e31576f43655044647671467875634b4173327873' \
               '666c6b69675061793347397968527561'
    SESSION.execute(f'''
    INSERT INTO "user" (id, email, "publicName", "canBookFreeOffers", "isAdmin", password, "postalCode", 
    "departementCode", "dateCreated", "needsToFillCulturalSurvey", "culturalSurveyFilledDate")
    VALUES ({id}, '{email}', '{public_name}', {can_book_free_offers}, {is_admin}, '{password}', '{postal_code}', 
    '{departement_code}', '{date_created}', {needs_to_fill_cultural_survey}, {cultural_survey_filled_date})
    ''')
    SESSION.commit()


def create_offerer(id=1, thumb_count=0, is_active=True, postal_code='93100', city='Montreuil',
                   date_created='2019-11-20',
                   name='Test Offerer', siren='123456789', fields_updated='{}'):
    SESSION.execute(f'''
    INSERT INTO offerer (id, "thumbCount", "isActive", "postalCode", city, "dateCreated", name, siren, "fieldsUpdated")
    VALUES ({id}, {thumb_count}, {is_active}, '{postal_code}', '{city}', '{date_created}', '{name}', '{siren}', '{fields_updated}')
    ''')
    SESSION.commit()


def create_venue(offerer_id, id=1, thumb_count=0, name='Test Venue', siret='12345678912345', postal_code='93',
                 city='Montreuil', departement_code='93', is_virtual=False, fields_updated='{}'):
    if not siret:
        siret = 'NULL'
    else:
        siret = f"'{siret}'"

    if not postal_code:
        postal_code = 'NULL'
    else:
        postal_code = f"'{postal_code}'"

    if not city:
        city = 'NULL'
    else:
        city = f"'{city}'"

    if not departement_code:
        departement_code = 'NULL'
    else:
        departement_code = f"'{departement_code}'"

    SESSION.execute(f'''
    INSERT INTO venue (id, "thumbCount", "name", "siret", "postalCode", city, "departementCode", "managingOffererId", "isVirtual", "fieldsUpdated")
    VALUES ({id}, {thumb_count}, '{name}', {siret}, {postal_code}, {city}, {departement_code}, {offerer_id}, {is_virtual}, '{fields_updated}')
    ''')
    SESSION.commit()


def create_product(id=1, thumb_count=0, product_type='ThingType.LIVRE_EDITION', name='Livre',
                   media_urls=['https://url.test', 'https://someurl.test'], fields_updated='{}',
                   url=None, is_national=False):
    SESSION.execute(f'''
            INSERT INTO product (id, "thumbCount", type, name, "mediaUrls", url, "isNational", "fieldsUpdated")
            VALUES ({id}, {thumb_count}, '{product_type}', '{name}', ARRAY{media_urls}, '{url}', {is_national}, '{fields_updated}')
            ''')
    SESSION.commit()


def create_offer(venue_id, product_id, id=1, is_active=True, product_type='ThingType.LIVRE_EDITION',
                 name='Livre', media_urls=['https://url.test', 'https://someurl.test'], url=None, is_national=False,
                 date_created='2019-11-20', is_duo=False, fields_updated='{}'):
    url='Null' if not url else f"'{url}'"
    SESSION.execute(f'''
                INSERT INTO offer (id, "venueId", "productId", "isActive", type, name, "mediaUrls", url, "isNational", "dateCreated", "isDuo", "fieldsUpdated")
                VALUES ({id}, {venue_id}, {product_id}, {is_active}, '{product_type}', '{name}', ARRAY{media_urls}, {url}, {is_national}, '{date_created}', {is_duo}, '{fields_updated}')
                ''')
    SESSION.commit()


def create_stock(offer_id, id=1, is_soft_deleted=False, date_modified='2019-11-20', date_created='2019-11-20', price=0,
                 available=10, groupe_size=1, booking_limit_datetime=None, beginning_datetime=None,
                 fields_updated='{}'):
    if not booking_limit_datetime:
        booking_limit_datetime = 'NULL'
    else:
        booking_limit_datetime = f"'{booking_limit_datetime}'"

    if not beginning_datetime:
        beginning_datetime = 'NULL'
    else:
        beginning_datetime = f"'{beginning_datetime}'"

    SESSION.execute(f'''
        INSERT INTO stock (id, "isSoftDeleted", "dateModified", "dateCreated", "offerId", price, available, "groupSize", "beginningDatetime", "bookingLimitDatetime", "fieldsUpdated")
        VALUES ({id}, {is_soft_deleted}, '{date_modified}', '{date_created}', {offer_id}, {price}, {available}, {groupe_size}, {beginning_datetime}, {booking_limit_datetime}, '{fields_updated}')
        ''')
    SESSION.commit()


def create_booking(user_id, stock_id, id=1, date_created='2019-11-20', quantity=1, token='ABC123', amount=0,
                   is_cancelled=False, is_used=False, date_used='2019-11-22'):
    SESSION.execute(f'''
            INSERT INTO booking (id, "dateCreated", "stockId", quantity, token, "userId", amount, "isCancelled", "isUsed", "dateUsed")
            VALUES ({id}, '{date_created}', {stock_id}, {quantity}, '{token}', {user_id}, {amount}, {is_cancelled}, {is_used}, '{date_used}')
            ''')
    SESSION.commit()


def create_mediation(offer_id, id=1, thumb_count=0, is_active=True, date_created='2019-11-20'):
    SESSION.execute(f'''
                INSERT INTO mediation (id, "thumbCount", "offerId", "isActive", "dateCreated")
                VALUES ({id}, {thumb_count}, {offer_id}, {is_active}, '{date_created}')
                ''')
    SESSION.commit()


def create_recommendation(offer_id, user_id, mediation_id='NULL', id=1, date_created='2019-11-20',
                          date_updated='2019-11-20', is_clicked=False, is_first=False):
    SESSION.execute(f'''
                INSERT INTO recommendation (id, "offerId", "userId", "mediationId", "dateCreated", "dateUpdated", "isClicked", "isFirst")
                VALUES ({id}, {offer_id}, {user_id}, {mediation_id}, '{date_created}', '{date_updated}', {is_clicked}, {is_first})
                ''')
    SESSION.commit()


def create_payment(booking_id, amount=10, reimbursement_rule='test', reimbursement_rate=1, recipient_name='Toto',
                   recipient_siren='123456789', author='test', id=1):
    SESSION.execute(f'''
                INSERT INTO payment (id, "bookingId", amount, "reimbursementRule", "reimbursementRate", "recipientName", "recipientSiren", author)
                VALUES ({id}, {booking_id}, {amount}, '{reimbursement_rule}', {reimbursement_rate}, '{recipient_name}' ,'{recipient_siren}', '{author}')
                ''')
    SESSION.commit()


def create_payment_status(payment_id, id=1, date='2019-11-29', status='PENDING'):
    SESSION.execute(f'''
                INSERT INTO payment_status (id, "paymentId", date, status)
                VALUES ({id}, {payment_id}, '{date}', '{status}')
                ''')
    SESSION.commit()


def create_deposit(id=1, amount=500, user_id=1, source='string', date_created='2019-11-29'):
    SESSION.execute(f'''
                INSERT INTO deposit (id, amount, "userId", source, "dateCreated")
                VALUES ({id}, {amount}, {user_id}, '{source}', '{date_created}')
                ''')
    SESSION.commit()


def update_table_column(id, table_name, column, value):
    SESSION.execute(f'''
            UPDATE {table_name} 
            SET {column} = ({value})
            WHERE id={id}
            ''')
    SESSION.commit()


def clean_database():
    SESSION.execute('''
    DELETE FROM "deposit";
    DELETE FROM "recommendation";
    DELETE FROM payment_status;
    DELETE FROM payment;
    DELETE FROM "booking";
    DELETE FROM "stock";
    DELETE FROM "offer";
    DELETE FROM "product";
    DELETE FROM "venue";
    DELETE FROM "mediation";
    DELETE FROM "offerer";
    DELETE FROM "user";
    DROP TABLE IF EXISTS enriched_offerer_data;
    DROP TABLE IF EXISTS enriched_user_data;
    DROP TABLE IF EXISTS enriched_stock_data;
    ''')
    SESSION.commit()



