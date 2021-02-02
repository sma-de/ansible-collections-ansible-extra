
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleOptionsError
from ansible.module_utils.six import iteritems, string_types

from ansible_collections.smabot.base.plugins.module_utils.plugins.config_normalizing.base import ConfigNormalizerBaseMerger, NormalizerBase, NormalizerNamed, DefaultSetterConstant, DefaultSetterOtherKey
from ansible_collections.smabot.base.plugins.module_utils.utils.dicting import setdefault_none, SUBDICT_METAKEY_ANY, get_subdict

from ansible_collections.smabot.base.plugins.module_utils.utils.utils import ansible_assert



class ConfigRootNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          ServerInstancesNormalizer(pluginref),
        ]

        super(ConfigRootNormalizer, self).__init__(pluginref, *args, **kwargs)


class ServerInstancesNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          SrvInstNormalizer(pluginref),
        ]

        super(ServerInstancesNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return ['instances']


class SrvInstNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          OrganizationsNormalizer(pluginref),
        ]

        super(SrvInstNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return [SUBDICT_METAKEY_ANY]


class OrganizationsNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          OrgaInstNormalizer(pluginref),
        ]

        super(OrganizationsNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return ['organizations']


class OrgaInstNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          JobNormalizer(pluginref),
        ]

        super(OrgaInstNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return [SUBDICT_METAKEY_ANY]


class JobNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        subnorms = kwargs.setdefault('sub_normalizers', [])
        subnorms += [
          JobCfgNormalizer(pluginref),
        ]

        super(JobNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return ['jobs', SUBDICT_METAKEY_ANY]


class JobCfgNormalizer(NormalizerBase):

    def __init__(self, pluginref, *args, **kwargs):
        super(JobCfgNormalizer, self).__init__(
           pluginref, *args, **kwargs
        )

    @property
    def config_path(self):
        return ['config']

    def _handle_specifics_presub(self, cfg, my_subcfg, cfgpath_abs):
        # default job pyenv
        pyenv = my_subcfg.get('virtual_pyenv', None)

        if not pyenv:
            pyenv_orga = self.get_parentcfg(cfg, cfgpath_abs, level=3)

            if pyenv_orga:
                my_subcfg['virtual_pyenv'] = pyenv_orga

        return my_subcfg



class ActionModule(ConfigNormalizerBaseMerger):

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(ConfigRootNormalizer(self), 
            *args, ##default_merge_vars=['gitlab_cfg_defaults'], 
            ##extra_merge_vars_ans=['extra_gitlab_config_maps'], 
            **kwargs
        )

        self._supports_check_mode = False
        self._supports_async = False


    @property
    def my_ansvar(self):
        return 'awx_cfg'

