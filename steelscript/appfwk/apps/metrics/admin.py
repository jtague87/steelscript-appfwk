# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


from django.contrib import admin

from steelscript.appfwk.apps.metrics.models import \
    NetworkMetric, ServicesMetric, ServiceNode


#
# Include in plugin admin.py
#

class NetworkMetricAdmin(admin.ModelAdmin):
    list_display = ('location', 'parent_group', 'parent_status',
                    'override_value', 'affected_nodes')
    fields = ('location', 'parent_group', 'parent_status', 'override_value')
    exclude = ('name',)

    def affected_nodes(self, obj):
        return obj.affected_nodes.all()

admin.site.register(NetworkMetric, NetworkMetricAdmin)


class ServiceNodeInline(admin.TabularInline):
    model = ServiceNode
    fields = ('name',)


class ServicesMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'override_value', 'affected_nodes')
    inlines = (ServiceNodeInline,)

    def affected_nodes(self, obj):
        return obj.affected_nodes.all()

admin.site.register(ServicesMetric, ServicesMetricAdmin)
