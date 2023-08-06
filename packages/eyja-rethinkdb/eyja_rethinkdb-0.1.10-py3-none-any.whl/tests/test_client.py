from unittest import IsolatedAsyncioTestCase

from rethinkdb import r

from eyja.main import Eyja
from eyja.hubs import DataHub
from eyja.interfaces.db import BaseStorageModel


class RethinkDBClientTest(IsolatedAsyncioTestCase):
    rethinkdb_connection = None

    config = '''
        storages:
            rethinkdb:
                port: 30001
                password: 123456
                db:
                -   test_db
    '''

    class TestModel(BaseStorageModel):
        _namespace = ':::test_table'
        _indexes = [
            'test_str'
        ] + BaseStorageModel._indexes
        
        test_str: str

    async def asyncSetUp(self):
        r.set_loop_type('asyncio')
        self.rethinkdb_connection = await r.connect(host='localhost', port=30001, password='123456')

    async def find_items(self, db, table, **filter):
        result = await r.db(db).table(table).filter(filter).run(self.rethinkdb_connection)
        return [item async for item in result]

    async def test_connection(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        db_list = await r.db_list().run(self.rethinkdb_connection)

        self.assertTrue(Eyja.is_initialized())
        self.assertIn('test_db', db_list)

    async def test_save_model(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        obj = self.TestModel(
            test_str='Test123'
        )
        await obj.save()

        table_list = await r.db('test_db').table_list().run(self.rethinkdb_connection)
        index_list = await r.db('test_db').table('test_table').index_list().run(self.rethinkdb_connection)
        saved_data = await self.find_items('test_db', 'test_table', test_str='Test123')

        self.assertIn('test_table', table_list)
        self.assertIn('test_str', index_list)
        self.assertEqual(len(saved_data), 1)

    async def test_delete_model(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        obj = self.TestModel(
            test_str='Test1'
        )
        await obj.save()
        await obj.delete()

        saved_data = await self.find_items('test_db', 'test_table', test_str='Test1')
        self.assertEqual(len(saved_data), 0)

    async def test_delete_all_models(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        await self.TestModel(test_str='Test2').save()
        await self.TestModel(test_str='Test2').save()
        await self.TestModel(test_str='Test2').save()
        await self.TestModel(test_str='Test22').save()
        await self.TestModel(test_str='Test22').save()

        await self.TestModel.delete_all({'test_str': 'Test2'})

        self.assertEqual(len(await self.find_items('test_db', 'test_table', test_str='Test2')), 0)
        self.assertEqual(len(await self.find_items('test_db', 'test_table', test_str='Test22')), 2)

    async def test_get_model(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        obj = self.TestModel(
            test_str='Test3'
        )
        await obj.save()

        get_obj = await self.TestModel.get(obj.object_id)

        self.assertEqual(get_obj.test_str, obj.test_str)

    async def test_find_models(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test44').save()
        await self.TestModel(test_str='Test44').save()

        self.assertEqual(len(await self.TestModel.find({'test_str': 'Test4'})), 3)
        self.assertEqual(len(await self.TestModel.find({'test_str': 'Test44'})), 2)

    async def test_find_models(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_rethinkdb']
        )

        await self.TestModel(test_str='Test5').save()
        await self.TestModel(test_str='Test5').save()
        await self.TestModel(test_str='Test5').save()
        await self.TestModel(test_str='Test55').save()
        await self.TestModel(test_str='Test55').save()

        self.assertEqual(await self.TestModel.count({'test_str': 'Test5'}), 3)
        self.assertEqual(await self.TestModel.count({'test_str': 'Test55'}), 2)
