import psycopg2
import psycopg2.extras
import datetime

from db import get_conn_cur, close


class Model(object):
    def __init__(self, **kwargs):
        if kwargs is None:
            raise ValueError("No details provided.")
        if kwargs['id'] is None:
            self.id = None
        else:
            try:
                self.id = kwargs["id"]
            except ValueError as e:
                print(e)
            finally:
                self.id = None

        for k in kwargs.keys():
            setattr(self, k, kwargs[k])

        self.fields = set()
        for k in dir(self):
            self.fields.add(k)

    def __setattr__(self, name, value):
        if name in dir(self):
            if value is not None:
                field_cls = type(getattr(self, name))
                if name == 'id':
                    field_cls = int
                super().__setattr__(name, field_cls(value))
        else:
            super().__setattr__(name, value)


class Region:
    """
    Region model
    """
    table_name = "Region"
    FIELDS = {
        "id": int,
        "region_number": int,
        "region_name": str
    }

    def __init__(self):

        if self.FIELDS is None:
            raise ValueError("No region details provided.")

        for name, value in self.FIELDS.items():
            super().__setattr__(name, value)

        self.fields = {}
        for field in self.FIELDS.keys():
            self.fields.update({field: None})

    def save(self, kwargs):
        if 'id' not in kwargs.keys() or kwargs['id'] is None:
            self.insert(kwargs=kwargs)
        else:
            self.update(kwargs=kwargs)

    def insert(self, kwargs):
        """
            INSERT method for Region table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        region_insert_template = "INSERT INTO \"Region\" (region_number, region_name) VALUES (%s, %s) RETURNING id;"

        id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:

            cur.execute(region_insert_template, (kwargs["region_number"], kwargs["region_name"]))
            id = cur.fetchone()
            conn.commit()
            # self.fields.up
            pass
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                if name is not 'id':
                    self.fields[name] = kwargs[name]
                else:
                    self.fields[name] = id['id']
            close(conn, cur)

    # TODO check if update id exists
    def update(self, kwargs):
        """
            UPDATE method for Region table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        region_update_template = "UPDATE \"Region\" SET region_number=%s, region_name=%s WHERE id=%s;"

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:
            cur.execute(region_update_template, (kwargs["region_number"], kwargs["region_name"], kwargs["id"]))
            conn.commit()
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                self.fields[name] = kwargs[name]
            close(conn, cur)

    def delete(self, kwargs=None):

        """
            Delete method for Region table
        :return:
        """

        conn, cur = get_conn_cur()
        region_delete_template = "DELETE FROM \"Region\"  WHERE id=%s;"
        id = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(region_delete_template, (id,))
                conn.commit()
            except psycopg2.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

    # TODO: add cols variance and WHERE with multiple cols filter
    def get_region(self, kwargs):

        conn, cur = get_conn_cur()
        cols = ','.join(self.FIELDS.keys())
        region_getitem_template = "SELECT {} FROM \"Region\" WHERE id=%s;".format(cols)

        id = None
        region_item = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(region_getitem_template, (id,))
                region_item = cur.fetchone()
            except psycopg2.DatabaseError as e:
                # conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

        if region_item or len(region_item) != 0:
            for name in self.FIELDS.keys():
                self.fields[name] = region_item[name]
        else:
            for name in self.FIELDS.keys():
                self.fields[name] = None

        return self.fields

    def get_regions(self, kwargs=None):
        conn, cur = get_conn_cur()
        region_getitems_template = "SELECT {} FROM \"Region\""

        regions = []

        cols = None
        order_by = None
        order_template = " ORDER BY {}"

        if kwargs:
            if 'cols' in kwargs.keys():
                cols = kwargs['cols']
            else:
                cols = '*'

            if kwargs['order']:
                order_by = kwargs['order']
                region_getitems_template += order_template.format(order_by)

        if not cols:
            cols = '*'

        if not order_by:
            order_by = 'id'

        region_getitems_template = region_getitems_template.format(cols)

        try:
            cur.execute(region_getitems_template, (order_by,))
            regions = cur.fetchall()
        except psycopg2.DatabaseError as e:
            # conn.rollback()
            raise e
        finally:
            close(conn, cur)

        return regions


class ItemComposition:
    """
    Item Composition model
    """
    table_name = "ItemComposition"
    FIELDS = {
        "id": int,
        "material": str,
        "weight": float
    }

    def __init__(self):

        if self.FIELDS is None:
            raise ValueError("No item composition details provided.")

        for name, value in self.FIELDS.items():
            super().__setattr__(name, value)

        self.fields = {}
        for field in self.FIELDS.keys():
            self.fields.update({field: None})

    def save(self, kwargs):
        if 'id' not in kwargs.keys() or kwargs['id'] is None:
            self.insert(kwargs=kwargs)
        else:
            self.update(kwargs=kwargs)

    def insert(self, kwargs):
        """
            INSERT method for ItemComposition table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        item_composition_insert_template = "INSERT INTO \"ItemComposition\" (material, weight) VALUES (%s, %s) RETURNING id;"

        id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:

            cur.execute(item_composition_insert_template, (kwargs["material"], kwargs["weight"]))
            id = cur.fetchone()
            conn.commit()
            # self.fields.up
            pass
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                if name is not 'id':
                    self.fields[name] = kwargs[name]
                else:
                    self.fields[name] = id['id']
            close(conn, cur)

    # TODO check if update id exists
    def update(self, kwargs):
        """
            UPDATE method for ItemComposition table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        item_composition_update_template = "UPDATE \"ItemComposition\" SET material=%s, weight=%s WHERE id=%s;"

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:
            cur.execute(item_composition_update_template, (kwargs["material"], kwargs["weight"], kwargs["id"]))
            conn.commit()
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                self.fields[name] = kwargs[name]
            close(conn, cur)

    def delete(self, kwargs=None):

        """
            Delete method for ItemComposition table
        :return:
        """

        conn, cur = get_conn_cur()
        item_composition_delete_template = "DELETE FROM \"ItemComposition\"  WHERE id=%s;"
        id = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(item_composition_delete_template, (id,))
                conn.commit()
            except psycopg2.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

    # TODO: add cols variance and WHERE with multiple cols filter
    def get_item_composition(self, kwargs):

        conn, cur = get_conn_cur()
        cols = ','.join(self.FIELDS.keys())
        item_composition_getitem_template = "SELECT {} FROM \"ItemComposition\" WHERE id=%s;".format(cols)

        id = None
        item_composition = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(item_composition_getitem_template, (id,))
                item_composition = cur.fetchone()
            except psycopg2.DatabaseError as e:
                # conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

        if item_composition or len(item_composition) != 0:
            for name in self.FIELDS.keys():
                self.fields[name] = item_composition[name]
        else:
            for name in self.FIELDS.keys():
                self.fields[name] = None

        return self.fields

    def get_items_composition(self, kwargs=None):
        conn, cur = get_conn_cur()
        item_composition_getitems_template = "SELECT {} FROM \"ItemComposition\""

        items_composition = []

        cols = None
        order_by = None
        order_template = " ORDER BY {}"

        if kwargs:
            if 'cols' in kwargs.keys():
                cols = kwargs['cols']
            else:
                cols = '*'

            if kwargs['order']:
                order_by = kwargs['order']
                item_composition_getitems_template += order_template.format(order_by)

        if not cols:
            cols = '*'

        if not order_by:
            order_by = 'id'

        item_composition_getitems_template = item_composition_getitems_template.format(cols)

        try:
            cur.execute(item_composition_getitems_template, (order_by,))
            items_composition = cur.fetchall()
        except psycopg2.DatabaseError as e:
            # conn.rollback()
            raise e
        finally:
            close(conn, cur)

        return items_composition


# TODO: byte field is not yet ready for usage
class JewelryShop:
    """
    Jewelry Shop model
    """
    table_name = "JewelryShop"
    FIELDS = {
        "id": int,
        "address": str,
        "license_copy": bytes,
        "schedule_day": str,
        "schedule_time": str,
    }

    def __init__(self):

        if self.FIELDS is None:
            raise ValueError("No jewelry shop details provided.")

        for name, value in self.FIELDS.items():
            super().__setattr__(name, value)

        self.fields = {}
        for field in self.FIELDS.keys():
            self.fields.update({field: None})

    def save(self, kwargs):
        if 'id' not in kwargs.keys() or kwargs['id'] is None:
            self.insert(kwargs=kwargs)
        else:
            self.update(kwargs=kwargs)

    def insert(self, kwargs):
        """
            INSERT method for JewelryShop table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        jewelry_shop_insert_template = "INSERT INTO \"JewelryShop\" (address, license_copy, schedule_day, schedule_time) VALUES (%s, %s, %s, %s) RETURNING id;"

        id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:
            cur.execute(jewelry_shop_insert_template,
                        (kwargs["address"], kwargs["license_copy"], kwargs["schedule_day"], kwargs["schedule_time"]))
            id = cur.fetchone()
            conn.commit()
            # self.fields.up
            pass
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                if name is not 'id':
                    self.fields[name] = kwargs[name]
                else:
                    self.fields[name] = id['id']
            close(conn, cur)

    # TODO check if update id exists
    def update(self, kwargs):
        """
            UPDATE method for JewelryShop table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        jewelry_shop_update_template = "UPDATE \"JewelryShop\" SET address=%s, license_copy=%s, schedule_day=%s, schedule_time=%s WHERE id=%s;"

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        try:
            cur.execute(jewelry_shop_update_template, (
                kwargs["address"], kwargs["license_copy"], kwargs["schedule_day"], kwargs["schedule_time"],
                kwargs["id"]))
            conn.commit()
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                self.fields[name] = kwargs[name]
            close(conn, cur)

    def delete(self, kwargs=None):

        """
            Delete method for JewelryShop table
        :return:
        """

        conn, cur = get_conn_cur()
        jewelry_shop_delete_template = "DELETE FROM \"JewelryShop\"  WHERE id=%s;"
        id = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(jewelry_shop_delete_template, (id,))
                conn.commit()
            except psycopg2.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

    # TODO: add cols variance and WHERE with multiple cols filter
    def get_jewelry_shop(self, kwargs):

        conn, cur = get_conn_cur()
        cols = ','.join(self.FIELDS.keys())
        jewelry_shop_getitem_template = "SELECT {} FROM \"JewelryShop\" WHERE id=%s;".format(cols)

        id = None
        jewelry_shop = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(jewelry_shop_getitem_template, (id,))
                jewelry_shop = cur.fetchone()
            except psycopg2.DatabaseError as e:
                # conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

        if jewelry_shop or len(jewelry_shop) != 0:
            for name in self.FIELDS.keys():
                self.fields[name] = jewelry_shop[name]
        else:
            for name in self.FIELDS.keys():
                self.fields[name] = None

        return self.fields

    def get_jewelry_shops(self, kwargs=None):
        conn, cur = get_conn_cur()
        jewelry_shops_getitems_template = "SELECT {} FROM \"ItemComposition\""

        jewelry_shops = []

        cols = None
        order_by = None
        order_template = " ORDER BY {}"

        if kwargs:
            if 'cols' in kwargs.keys():
                cols = kwargs['cols']
            else:
                cols = '*'

            if kwargs['order']:
                order_by = kwargs['order']
                jewelry_shops_getitems_template += order_template.format(order_by)

        if not cols:
            cols = '*'

        if not order_by:
            order_by = 'id'

        jewelry_shops_getitems_template = jewelry_shops_getitems_template.format(cols)

        try:
            cur.execute(jewelry_shops_getitems_template, (order_by,))
            jewelry_shops = cur.fetchall()
        except psycopg2.DatabaseError as e:
            # conn.rollback()
            raise e
        finally:
            close(conn, cur)

        return jewelry_shops


class ProducerCompany:
    """
    Producer company model
    """
    table_name = "ProducerCompany"
    FIELDS = {
        "id": int,
        "company_name": str,
        "region": dict
    }

    def __init__(self):

        if self.FIELDS is None:
            raise ValueError("No producer company details provided.")

        for name, value in self.FIELDS.items():
            super().__setattr__(name, value)

        self.fields = {}
        for field in self.FIELDS.keys():
            self.fields.update({field: None})

    def save(self, kwargs):
        if 'id' not in kwargs.keys() or kwargs['id'] is None:
            self.insert(kwargs=kwargs)
        else:
            self.update(kwargs=kwargs)

    def insert(self, kwargs):
        """
            INSERT method for Producer company table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        producer_insert_template = "INSERT INTO \"ProducerCompany\" (company_name, region) VALUES (%s, %s) RETURNING id;"

        id = None
        regions_id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    if name is not 'region':
                        kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        if kwargs:
            if 'region' in kwargs.keys():
                if isinstance(kwargs['region'], int):
                    regions_id = kwargs['region']

        try:
            r = Region()
            if not regions_id:
                r.save(kwargs=kwargs['region'])
                regions_id = r.fields['id']
                kwargs['region'].update({'id': regions_id})
            elif not r.get_region(kwargs={'id': regions_id}).get('id'):
                raise IndexError('No elements with id={}'.format(regions_id))

            cur.execute(producer_insert_template, (kwargs["company_name"], regions_id,))
            id = cur.fetchone()
            conn.commit()
            # self.fields.up
            pass
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                if name is not 'id':
                    self.fields[name] = kwargs[name]
                else:
                    self.fields[name] = id['id']
            close(conn, cur)

    def update(self, kwargs):
        """
            UPDATE method for Producer company table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        region_update_template = "UPDATE \"ProducerCompany\" SET company_name=%s, region=%s WHERE id=%s;"

        regions_id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        if kwargs:
            if 'region' in kwargs.keys():
                if isinstance(kwargs['region'], int):
                    regions_id = kwargs['region']

        try:
            r = Region()
            if not regions_id:
                r.save(kwargs=kwargs['region'])
                regions_id = r.fields['id']
            elif not r.get_region(kwargs={'id': regions_id}).get('id'):
                raise IndexError('No elements with id={}'.format(regions_id))

            cur.execute(region_update_template, (kwargs["company_name"], regions_id, kwargs['id']))
            conn.commit()
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                self.fields[name] = kwargs[name]
            close(conn, cur)

    def delete(self, kwargs=None):

        """
            Delete method for Producer company table
        :return:
        """

        conn, cur = get_conn_cur()
        producer_delete_template = "DELETE FROM \"ProducerCompany\"  WHERE id=%s;"
        id = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(producer_delete_template, (id,))
                conn.commit()
            except psycopg2.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

    # TODO: add cols variance and WHERE with multiple cols filter
    def get_producer(self, kwargs):

        conn, cur = get_conn_cur()
        cols = ','.join(self.FIELDS.keys())
        producer_getitem_template = "SELECT {} FROM \"ProducerCompany\" WHERE id=%s;".format(cols)

        id = None
        producer_item = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(producer_getitem_template, (id,))
                producer_item = cur.fetchone()
                r = Region()
                region = r.get_region(kwargs={'id': producer_item['region']})
                producer_item['region'] = region
            except psycopg2.DatabaseError as e:
                # conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

        if producer_item:
            for name in self.FIELDS.keys():
                self.fields[name] = producer_item[name]
        else:
            for name in self.FIELDS.keys():
                self.fields[name] = None

        return self.fields

    def get_producers(self, kwargs=None):
        conn, cur = get_conn_cur()
        producer_getitems_template = "SELECT {} FROM \"ProducerCompany\""

        producers = []

        cols = None
        order_by = None
        order_template = " ORDER BY {}"

        if kwargs:
            if 'cols' in kwargs.keys():
                cols = kwargs['cols']
            else:
                cols = '*'

            if kwargs['order']:
                order_by = kwargs['order']
                producer_getitems_template += order_template.format(order_by)

        if not cols:
            cols = '*'

        if not order_by:
            order_by = 'id'

        producer_getitems_template = producer_getitems_template.format(cols)

        try:
            cur.execute(producer_getitems_template, (order_by,))
            producers_db = cur.fetchall()
            r = Region()
            for row in producers_db:
                new_dict = dict(row)
                reg_dict = dict(r.get_region(kwargs={'id': new_dict['region']}))
                new_dict['region'] = reg_dict
                producers.append(new_dict)
        except psycopg2.DatabaseError as e:
            # conn.rollback()
            raise e
        finally:
            close(conn, cur)

        return producers


class JewelryItem:
    """
    Jewelry item model
    """
    table_name = "JewelryItem"
    FIELDS = {
        "id": int,
        "item_type": str,
        "item_weight": float,
        "item_probe": int,
        "company_producer": dict,
        "item_arrive_date": float,
        "item_cost": float,
        "item_composition": int,
    }

    def __init__(self):

        if self.FIELDS is None:
            raise ValueError("No producer company details provided.")

        for name, value in self.FIELDS.items():
            super().__setattr__(name, value)

        self.fields = {}
        for field in self.FIELDS.keys():
            self.fields.update({field: None})

    def save(self, kwargs):
        if 'id' not in kwargs.keys() or kwargs['id'] is None:
            self.insert(kwargs=kwargs)
        else:
            self.update(kwargs=kwargs)

    def insert(self, kwargs):
        """
            INSERT method for Jewelry item table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        jewelry_item_insert_template = "INSERT INTO \"JewelryItem\" (item_type, item_weight, item_probe," \
                                       " company_producer, item_arrive_date, item_cost, item_composition)" \
                                       " VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"

        id = None
        company_producer_id = None
        item_composition_id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    if name not in ['company_producer', 'item_composition']:
                        kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        if kwargs:
            if 'company_producer' in kwargs.keys():
                if isinstance(kwargs['company_producer'], int):
                    company_producer_id = kwargs['company_producer']
            if 'item_composition' in kwargs.keys():
                if isinstance(kwargs['item_composition'], int):
                    item_composition_id = kwargs['item_composition']

        try:
            prod = ProducerCompany()
            item_comp = ItemComposition()
            if not company_producer_id:
                prod.save(kwargs=kwargs['company_producer'])
                company_producer_id = prod.fields['id']
                kwargs['company_producer'].update({'id': company_producer_id})
            elif not prod.get_producer(kwargs={'id': company_producer_id}).get('id'):
                raise IndexError('No elements with id={}'.format(company_producer_id))

            if not item_composition_id:
                item_comp.save(kwargs=kwargs['item_composition'])
                item_composition_id = item_comp.fields['id']
                kwargs['item_composition'].update({'id': item_composition_id})
            elif not item_comp.get_item_composition(kwargs={'id': item_composition_id}).get('id'):
                raise IndexError('No elements with id={}'.format(item_composition_id))

            cur.execute(jewelry_item_insert_template, (kwargs['item_type'], kwargs['item_weight'], kwargs['item_probe'],
                                                       company_producer_id, kwargs['item_arrive_date'],
                                                       kwargs['item_cost'], item_composition_id))
            id = cur.fetchone()
            conn.commit()
            # self.fields.up
            pass
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                if name is not 'id':
                    self.fields[name] = kwargs[name]
                else:
                    self.fields[name] = id['id']
            close(conn, cur)

    def update(self, kwargs):
        """
            UPDATE method for Jewelry Item table
        :param kwargs:
        :return: values of model fields
        """
        conn, cur = get_conn_cur()
        jewelry_item_update_template = "UPDATE \"JewelryItem\" SET item_type=%s, item_weight=%s, item_probe=%s, \
                                        company_producer=%s, item_arrive_date=%s, item_cost=%s, item_composition=%s WHERE id=%s;"

        company_producer_id = None
        item_composition_id = None

        try:
            for name, value in kwargs.items():
                if name in self.FIELDS.keys():
                    kwargs[name] = self.FIELDS[name](value)
        except ValueError as e:
            raise e

        if kwargs:
            if 'company_producer' in kwargs.keys():
                if isinstance(kwargs['company_producer'], int):
                    company_producer_id = kwargs['company_producer']
            if 'item_composition' in kwargs.keys():
                if isinstance(kwargs['item_composition'], int):
                    item_composition_id = kwargs['item_composition']

        try:
            prod = ProducerCompany()
            item_comp = ItemComposition()
            if not company_producer_id:
                prod.save(kwargs=kwargs['company_producer'])
                company_producer_id = prod.fields['id']
            elif not prod.get_producer(kwargs={'id': company_producer_id}).get('id'):
                raise IndexError('No elements with id={}'.format(company_producer_id))

            if not item_composition_id:
                item_comp.save(kwargs=kwargs['item_composition'])
                item_composition_id = item_comp.fields['id']
            elif not item_comp.get_item_composition(kwargs={'id': item_composition_id}).get('id'):
                raise IndexError('No elements with id={}'.format(item_composition_id))

            cur.execute(jewelry_item_update_template, (kwargs['item_type'], kwargs['item_weight'], kwargs['item_probe'],
                                                       company_producer_id, kwargs['item_arrive_date'],
                                                       kwargs['item_cost'], item_composition_id, kwargs['id']))
            conn.commit()
        except psycopg2.DatabaseError as e:
            conn.rollback()
            raise e
        finally:
            for name in self.fields.keys():
                self.fields[name] = kwargs[name]
            close(conn, cur)

    def delete(self, kwargs=None):

        """
            Delete method for Jewelry item table
        :return:
        """

        conn, cur = get_conn_cur()
        jewelry_item_delete_template = "DELETE FROM \"JewelryItem\"  WHERE id=%s;"
        id = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(jewelry_item_delete_template, (id,))
                conn.commit()
            except psycopg2.DatabaseError as e:
                conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

    # TODO: add cols variance and WHERE with multiple cols filter
    def get_jewelry_item(self, kwargs):

        conn, cur = get_conn_cur()
        cols = ','.join(self.FIELDS.keys())
        jewelry_item_getitem_template = "SELECT {} FROM \"JewelryItem\" WHERE id=%s;".format(cols)

        id = None
        jewelry_item = None

        if kwargs:
            if 'id' not in kwargs.keys():
                if self.fields['id'] is not None:
                    id = self.fields['id']
            else:
                id = int(kwargs['id'])
        if id:
            try:
                cur.execute(jewelry_item_getitem_template, (id,))
                jewelry_item = cur.fetchone()
                prod = ProducerCompany()
                item_comp = ItemComposition()
                producer = prod.get_producer(kwargs={'id': jewelry_item['company_producer']})
                item_composition = item_comp.get_item_composition(kwargs={'id': jewelry_item['item_composition']})
                jewelry_item['company_producer'] = producer
                jewelry_item['item_composition'] = item_composition
            except psycopg2.DatabaseError as e:
                # conn.rollback()
                raise e
            finally:
                for name in self.fields.keys():
                    self.fields[name] = None
                close(conn, cur)

        if jewelry_item:
            for name in self.FIELDS.keys():
                self.fields[name] = jewelry_item[name]
        else:
            for name in self.FIELDS.keys():
                self.fields[name] = None

        return self.fields

    def get_jewelry_items(self, kwargs=None):
        conn, cur = get_conn_cur()
        jewelry_item_getitems_template = "SELECT {} FROM \"JewelryItem\""

        producers = []

        cols = None
        order_by = None
        order_template = " ORDER BY {}"

        if kwargs:
            if 'cols' in kwargs.keys():
                cols = kwargs['cols']
            else:
                cols = '*'

            if kwargs['order']:
                order_by = kwargs['order']
                jewelry_item_getitems_template += order_template.format(order_by)

        if not cols:
            cols = '*'

        if not order_by:
            order_by = 'id'

        jewelry_item_getitems_template = jewelry_item_getitems_template.format(cols)

        try:
            cur.execute(jewelry_item_getitems_template, (order_by,))
            producers_db = cur.fetchall()
            prod = ProducerCompany()
            item_comp = ItemComposition()
            for row in producers_db:
                new_dict = dict(row)
                prod_dict = dict(prod.get_producer(kwargs={'id': new_dict['company_producer']}))
                it_comp_dict = dict(item_comp.get_item_composition(kwargs={'id': new_dict['item_composition']}))
                new_dict['company_producer'] = prod_dict
                new_dict['item_composition'] = it_comp_dict
                producers.append(new_dict)
        except psycopg2.DatabaseError as e:
            # conn.rollback()
            raise e
        finally:
            close(conn, cur)

        return producers
