import redis
from itertools import zip_longest
import msgpack
import msgpack_numpy as m


class RedisStorage(object):
    def __init__(self, password="", host="127.0.0.1", port=6379, db=0, testing=False, keysplit="|", batch_size=100):
        """RedisStorage

        Args:
            password (str, optional): Redis Password. Defaults to "".
            host (str, optional): Redis Host Address. Defaults to "127.0.0.1".
            port (int, optional): Redis Port. Defaults to 6379.
            db (int, optional): Redis Db. Defaults to 0.
            testing (bool, optional): Using a in-memory redis alternative. Use Only for testing. Defaults to False.
            keysplit (str, optional): Char value use to split de keys values. Defaults to "|".
            batch_size (int, optional): Batch size use to process query. Defaults to 100.
        """
        self.keysplit = keysplit
        self.batch_size = batch_size
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        if not testing:
            self.redis_db = redis.Redis(
                host=self.host, port=self.port, db=self.db, password=self.password)
        else:
            import fakeredis
            self.redis_db = fakeredis.FakeStrictRedis()
        try:
            self.is_connected = self.redis_db.ping()
        except:
            self.is_connected = False

    def __repr__(self):
        """String Representation of the object

        Returns:
            [str]: [description]
        """
        if self.is_connected:
            return 'RedisStorage Host {} Port {} Db {} Password *******'.format(self.host, self.port, self.db)
        else:
            return "RedisStorage Not connected"

    def __getitem__(self, item):
        """Get values in the form obj["k1","k2","k3",..."kn"]

        Args:
            item ([string tuple]): the key index values

        Raises:
            Exception: If the redis db is Not Connected raise an Exception

        Returns:
            [list of numpy]: A list of values
        """
        if not self.is_connected:
            raise Exception("Not connected")
        params_list = list(item)
        params_length = len(params_list)
        params_key = self.keysplit.join(params_list)
        if self.contains_wildcard(params_key):
            # iteration data
            result = []
            for keybatch in self.redis_db.scan_iter(params_key):
                if keybatch is not None:
                    value = self.redis_db.get(keybatch)
                    result.append(msgpack.unpackb(value, object_hook=m.decode)) # 
            return result
        else:
            # single item
            value = self.redis_db.get(params_key)
            if value is None:
                return None
            return msgpack.unpackb(value, object_hook=m.decode) # 

    def __setitem__(self, item, value):
        """Store the value in the form obj["k1","k2","k3",..."kn"]= value

        Args:
            item ([string tuple]): Keys
            value ([numpy]): numpy value

        Raises:
            Exception: If the redis db is Not Connected raise an Exception
            Exception: if the value is not an numpy object
        """
        if not self.is_connected:
            raise Exception("Not connected")
        if str(type(value))!="<class 'numpy.ndarray'>":
            raise Exception("Value is not an numpy.ndarray object")
        params_list = list(item)
        params_length = len(params_list)
        params_key = self.keysplit.join(params_list)
        if self.contains_wildcard(params_key):
            # iteration data
            for keybatch in self.redis_db.scan_iter(params_key):
                if keybatch is not None:
                    self.redis_db.set(keybatch, msgpack.packb(value, default=m.encode)) # 
        else:
            # single item
            self.redis_db.set(params_key, msgpack.packb(value, default=m.encode)) # 

    def __delitem__(self, item):
        """Delete the values in the form obj["k1","k2","k3",..."kn"]

        Args:
            item ([str tuples]):Key values

        Raises:
            Exception:  Exception: If the redis db is Not Connected raise an Exception
        """
        if not self.is_connected:
            raise Exception("Not connected")
        params_list = list(item)
        params_length = len(params_list)
        params_key = self.keysplit.join(params_list)
        if self.contains_wildcard(params_key):
            # iteration data
            for keybatch in self.redis_db.scan_iter(params_key):
                if keybatch is not None:
                    self.redis_db.delete(keybatch)
        else:
            # single item
            self.redis_db.delete(params_key)

    def contains_wildcard(self, cad):
        """Check if cad have wildcard *

        Args:
            cad ([str]): str value 

        Returns:
            [boolean]: [description]
        """ 
        if '*' in cad:
            return True
        return False

    def batcher(self, iterable, n):
        """Create an iterate a list in batches of size n

        Args:
            iterable ([iterable]): iterable object
            n ([number]): size of the batch

        Returns:
            [zip_longest]: zip_longest of size n to iterate
        """
        args = [iter(iterable)] * n
        return zip_longest(*args)
