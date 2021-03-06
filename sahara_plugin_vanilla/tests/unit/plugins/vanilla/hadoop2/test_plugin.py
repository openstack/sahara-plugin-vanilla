# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock

from sahara.plugins import base as pb
from sahara.plugins import conductor
from sahara.plugins import context
from sahara.plugins import edp
from sahara_plugin_vanilla.tests.unit import base


class VanillaPluginTest(base.SaharaWithDbTestCase):
    def setUp(self):
        super(VanillaPluginTest, self).setUp()
        self.override_config("plugins", ["vanilla"])
        pb.setup_plugins()

    @mock.patch('sahara.plugins.edp.create_dir_hadoop2')
    def test_edp_calls_hadoop2_create_dir(self, create_dir):
        for version in ['2.7.1']:
            cluster_dict = {
                'name': 'cluster' + version.replace('.', '_'),
                'plugin_name': 'vanilla',
                'hadoop_version': version,
                'default_image_id': 'image'}

            cluster = conductor.cluster_create(context.ctx(), cluster_dict)
            plugin = pb.PLUGINS.get_plugin(cluster.plugin_name)
            create_dir.reset_mock()
            plugin.get_edp_engine(cluster, edp.JOB_TYPE_PIG).create_hdfs_dir(
                mock.Mock(), '/tmp')
            self.assertEqual(1, create_dir.call_count)
