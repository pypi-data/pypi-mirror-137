from unittest import IsolatedAsyncioTestCase

from eyja.main import Eyja
from eyja.hubs import DataHub
from eyja.interfaces.db import BaseStorageModel


class FileDBClientTest(IsolatedAsyncioTestCase):
    filedb_connection = None

    config = '''
        storages:
            filedb:
                path: ./tests/test.json
                db:
                -   test_db
    '''

    class TestModel(BaseStorageModel):
        _namespace = ':::test_table'
        
        test_str: str

    async def asyncSetUp(self):
        pass

    async def test_connection(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_filedb']
        )

        self.assertTrue(Eyja.is_initialized())

    async def test_save_model(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_filedb']
        )

        obj = self.TestModel(
            test_str='Test123'
        )
        await obj.save()

        new_obj = await self.TestModel.get(obj.object_id)

        self.assertEqual(obj.test_str, new_obj.test_str)

    async def test_find_models(self):
        await Eyja.reset()
        await Eyja.init(
            config=self.config,
            plugins=['eyja_filedb']
        )

        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test4').save()
        await self.TestModel(test_str='Test44').save()
        await self.TestModel(test_str='Test44').save()

        self.assertEqual(len(await self.TestModel.find({'test_str': 'Test4'})), 3)
        self.assertEqual(len(await self.TestModel.find({'test_str': 'Test44'})), 2)
