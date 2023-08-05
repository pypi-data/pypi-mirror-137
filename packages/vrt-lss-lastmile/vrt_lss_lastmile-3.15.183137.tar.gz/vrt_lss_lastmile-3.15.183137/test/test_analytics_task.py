# coding: utf-8

"""
    Veeroute.Lastmile

    Veeroute Lastmile API  # noqa: E501

    The version of the OpenAPI document: 3.15.183137
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_lastmile
from vrt_lss_lastmile.models.analytics_task import AnalyticsTask  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestAnalyticsTask(unittest.TestCase):
    """AnalyticsTask unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AnalyticsTask
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.analytics_task.AnalyticsTask()  # noqa: E501
        if include_optional :
            return AnalyticsTask(
                plan_task = {"locations":[{"key":"whs","location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_1","location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_2","location":{"latitude":55.839876,"longitude":37.629588,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_3","location":{"latitude":55.83022,"longitude":37.623083,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]}],"orders":[{"key":"order_1","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["B1"],"cargos":[{"key":"cargo_1","capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3},"width":1,"height":0.3,"length":2.2,"restrictions":["Freezer"]}],"demands":[{"key":"demand_1","demand_type":"PICKUP","target_cargos":["cargo_1"],"possible_events":[{"location_key":"whs","duration":10,"time_window":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T23:10:00Z"},"reward":1000}]},{"key":"demand_2","demand_type":"DROP","target_cargos":["cargo_1"],"possible_events":[{"location_key":"loc_1","duration":10,"time_window":{"from":"2021-05-13T06:00:00Z","to":"2021-05-13T23:10:00Z"},"reward":1000}]}]},{"key":"order_2","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["B1"],"cargos":[{"key":"cargo_2","capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3},"width":1,"height":0.3,"length":2.2,"restrictions":["Freezer"]}],"demands":[{"key":"demand_3","demand_type":"PICKUP","target_cargos":["cargo_2"],"possible_events":[{"location_key":"whs","duration":10,"time_window":{"from":"2021-05-13T05:00:00Z","to":"2021-05-13T22:20:00Z"},"reward":1000}]},{"key":"demand_4","demand_type":"DROP","target_cargos":["cargo_2"],"possible_events":[{"location_key":"loc_2","duration":10,"time_window":{"from":"2021-05-13T05:00:00Z","to":"2021-05-13T23:20:00Z"},"reward":1000}]}]},{"key":"order_3","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["work"],"cargos":[],"demands":[{"key":"demand_5","demand_type":"WORK","target_cargos":[],"possible_events":[{"location_key":"loc_3","duration":10,"time_window":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T22:10:00Z"},"reward":1000}]}]}],"performers":[{"key":"perf_1","max_work_shifts":3,"performer_features":["B1","Special","work"],"transport_restrictions":["B1"]},{"key":"perf_2","max_work_shifts":3,"performer_features":["B1","Special"],"transport_restrictions":["B1"]}],"transports":[{"key":"transp_1","transport_type":"CAR","transport_features":["20T","14T","B1"],"performer_restrictions":["B1"],"boxes":[{"key":"box01","capacity":{"mass":1000,"volume":200,"capacity_x":10,"capacity_y":20,"capacity_z":30},"width":1000,"height":20,"length":30,"features":["Freezer","SPB"]}]},{"key":"transp_2","transport_type":"CAR","transport_features":["20T","14T","B1"],"performer_restrictions":["B1"],"boxes":[{"key":"box02","capacity":{"mass":1000,"volume":200,"capacity_x":10,"capacity_y":20,"capacity_z":30},"width":100,"height":20,"length":30,"features":["Freezer","SPB"]}]}],"shifts":[{"key":"shift_1","shift_type":"PERFORMER","resource_key":"perf_1","availability_time":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"loc_1","finish_location_key":"loc_1","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_2","shift_type":"PERFORMER","resource_key":"perf_2","availability_time":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"loc_1","finish_location_key":"loc_1","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_3","shift_type":"TRANSPORT","resource_key":"transp_1","availability_time":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T09:00:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"whs","finish_location_key":"whs","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_4","shift_type":"TRANSPORT","resource_key":"transp_2","availability_time":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T09:00:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"whs","finish_location_key":"whs","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}}],"hardlinks":[{"key":"link_1","links":[{"type":"ORDER","entity_key":"order_1"},{"type":"ORDER","entity_key":"order_2"}]}],"settings":{"configuration":"optimize_distance"}}, 
                plan_result = {"tracedata":{"code":"example_LssTestingPreview_LastmileServicePlanner_2021-05-25-13-43_c83f103d-e59c-4d87-add9-635162bec755"},"trips":[{"key":"trip_shift_1","assigned_shifts":[{"shift_key":"shift_1","shift_time":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},{"shift_key":"shift_3","shift_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T12:01:00Z"}}],"actions":[{"order_key":"order_2","demand_key":"demand_3","location_key":"whs","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T10:30:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T10:30:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T10:30:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T10:40:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_2"}]},{"order_key":"order_1","demand_key":"demand_1","location_key":"whs","todolist":[{"job_type":"READY_TO_WORK","job_time":"2021-05-13T10:40:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T10:40:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T10:50:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T10:50:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_1"}]},{"order_key":"order_3","demand_key":"demand_5","location_key":"loc_3","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:00:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:00:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:00:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:10:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:10:00Z"}],"cargo_placements":[]},{"order_key":"order_1","demand_key":"demand_2","location_key":"loc_1","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:18:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:18:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:18:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:28:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:28:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_1"}]},{"order_key":"order_2","demand_key":"demand_4","location_key":"loc_2","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:41:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:41:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:41:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:51:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:51:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_2"}]}],"waitlist":[],"start_location_key":"loc_1","finish_location_key":"loc_1"}],"statistics":{"total_statistics":{"cost":15785.5,"reward":5000,"measurements":{"driving_time":52,"waiting_time":0,"working_time":50,"arriving_time":6,"departure_time":6,"total_time":114,"distance":7743,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},"orders_count":3,"plan_orders_count":3,"waitlist_orders_count":0,"performers_count":1,"capacity_utilization":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"quality":{"soft_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}},"hard_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}}}},"trips_statistics":[{"trip_key":"trip_shift_1","statistics":{"cost":15785.5,"reward":5000,"measurements":{"driving_time":52,"waiting_time":0,"working_time":50,"arriving_time":6,"departure_time":6,"total_time":114,"distance":7743,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},"orders_count":3,"plan_orders_count":3,"waitlist_orders_count":0,"performers_count":1,"capacity_utilization":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"capacity_max":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"quality":{"soft_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}},"hard_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}}}},"stop_statistics":[{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":[],"measurements":{"driving_time":0,"waiting_time":0,"working_time":0,"arriving_time":0,"departure_time":1,"total_time":1,"distance":1125,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T10:21:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"location_key":"whs","demand_ids":["order_2#demand_3","order_1#demand_1"],"measurements":{"driving_time":10,"waiting_time":0,"working_time":20,"arriving_time":1,"departure_time":1,"total_time":32,"distance":0,"time_window":{"from":"2021-05-13T10:29:00Z","to":"2021-05-13T10:51:00Z"}},"upload":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}},{"location":{"latitude":55.83022,"longitude":37.623083,"arrival_duration":1,"departure_duration":1},"location_key":"loc_3","demand_ids":["order_3#demand_5"],"measurements":{"driving_time":8,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":20,"distance":1594,"time_window":{"from":"2021-05-13T10:59:00Z","to":"2021-05-13T11:11:00Z"}},"current_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}},{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":["order_1#demand_2"],"measurements":{"driving_time":6,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":18,"distance":764,"time_window":{"from":"2021-05-13T11:17:00Z","to":"2021-05-13T11:29:00Z"}},"download":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}},"current_load":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}}},{"location":{"latitude":55.839876,"longitude":37.629588,"arrival_duration":1,"departure_duration":1},"location_key":"loc_2","demand_ids":["order_2#demand_4"],"measurements":{"driving_time":11,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":23,"distance":1905,"time_window":{"from":"2021-05-13T11:40:00Z","to":"2021-05-13T11:52:00Z"}},"download":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"location_key":"whs","demand_ids":[],"measurements":{"driving_time":9,"waiting_time":0,"working_time":0,"arriving_time":1,"departure_time":1,"total_time":11,"distance":1230,"time_window":{"from":"2021-05-13T12:00:00Z","to":"2021-05-13T12:02:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":[],"measurements":{"driving_time":8,"waiting_time":0,"working_time":0,"arriving_time":1,"departure_time":0,"total_time":9,"distance":1125,"time_window":{"from":"2021-05-13T12:09:00Z","to":"2021-05-13T12:10:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}}],"total_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}},"max_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}}]},"validations":[],"unplanned_orders":[],"progress":100,"info":{"status":"FINISHED_IN_TIME","result_version":0,"planning_time":0,"waiting_time":0}}
            )
        else :
            return AnalyticsTask(
                plan_task = {"locations":[{"key":"whs","location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_1","location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_2","location":{"latitude":55.839876,"longitude":37.629588,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]},{"key":"loc_3","location":{"latitude":55.83022,"longitude":37.623083,"arrival_duration":1,"departure_duration":1},"transport_restrictions":["14T"],"load_windows":[{"time_window":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"}}]}],"orders":[{"key":"order_1","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["B1"],"cargos":[{"key":"cargo_1","capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3},"width":1,"height":0.3,"length":2.2,"restrictions":["Freezer"]}],"demands":[{"key":"demand_1","demand_type":"PICKUP","target_cargos":["cargo_1"],"possible_events":[{"location_key":"whs","duration":10,"time_window":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T23:10:00Z"},"reward":1000}]},{"key":"demand_2","demand_type":"DROP","target_cargos":["cargo_1"],"possible_events":[{"location_key":"loc_1","duration":10,"time_window":{"from":"2021-05-13T06:00:00Z","to":"2021-05-13T23:10:00Z"},"reward":1000}]}]},{"key":"order_2","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["B1"],"cargos":[{"key":"cargo_2","capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3},"width":1,"height":0.3,"length":2.2,"restrictions":["Freezer"]}],"demands":[{"key":"demand_3","demand_type":"PICKUP","target_cargos":["cargo_2"],"possible_events":[{"location_key":"whs","duration":10,"time_window":{"from":"2021-05-13T05:00:00Z","to":"2021-05-13T22:20:00Z"},"reward":1000}]},{"key":"demand_4","demand_type":"DROP","target_cargos":["cargo_2"],"possible_events":[{"location_key":"loc_2","duration":10,"time_window":{"from":"2021-05-13T05:00:00Z","to":"2021-05-13T23:20:00Z"},"reward":1000}]}]},{"key":"order_3","order_features":["Special"],"order_restrictions":["Special"],"performer_restrictions":["work"],"cargos":[],"demands":[{"key":"demand_5","demand_type":"WORK","target_cargos":[],"possible_events":[{"location_key":"loc_3","duration":10,"time_window":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T22:10:00Z"},"reward":1000}]}]}],"performers":[{"key":"perf_1","max_work_shifts":3,"performer_features":["B1","Special","work"],"transport_restrictions":["B1"]},{"key":"perf_2","max_work_shifts":3,"performer_features":["B1","Special"],"transport_restrictions":["B1"]}],"transports":[{"key":"transp_1","transport_type":"CAR","transport_features":["20T","14T","B1"],"performer_restrictions":["B1"],"boxes":[{"key":"box01","capacity":{"mass":1000,"volume":200,"capacity_x":10,"capacity_y":20,"capacity_z":30},"width":1000,"height":20,"length":30,"features":["Freezer","SPB"]}]},{"key":"transp_2","transport_type":"CAR","transport_features":["20T","14T","B1"],"performer_restrictions":["B1"],"boxes":[{"key":"box02","capacity":{"mass":1000,"volume":200,"capacity_x":10,"capacity_y":20,"capacity_z":30},"width":100,"height":20,"length":30,"features":["Freezer","SPB"]}]}],"shifts":[{"key":"shift_1","shift_type":"PERFORMER","resource_key":"perf_1","availability_time":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"loc_1","finish_location_key":"loc_1","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_2","shift_type":"PERFORMER","resource_key":"perf_2","availability_time":{"from":"2021-05-13T09:30:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"loc_1","finish_location_key":"loc_1","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_3","shift_type":"TRANSPORT","resource_key":"transp_1","availability_time":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T09:00:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"whs","finish_location_key":"whs","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}},{"key":"shift_4","shift_type":"TRANSPORT","resource_key":"transp_2","availability_time":{"from":"2021-05-13T08:00:00Z","to":"2021-05-13T19:45:00Z"},"working_time":{"from":"2021-05-13T09:00:00Z","to":"2021-05-13T18:45:00Z"},"start_location_key":"whs","finish_location_key":"whs","tariff":{"cost_per_shift":2000,"constraints":[{"stage_length":40000,"cost_per_unit":1.5}]}}],"hardlinks":[{"key":"link_1","links":[{"type":"ORDER","entity_key":"order_1"},{"type":"ORDER","entity_key":"order_2"}]}],"settings":{"configuration":"optimize_distance"}},
                plan_result = {"tracedata":{"code":"example_LssTestingPreview_LastmileServicePlanner_2021-05-25-13-43_c83f103d-e59c-4d87-add9-635162bec755"},"trips":[{"key":"trip_shift_1","assigned_shifts":[{"shift_key":"shift_1","shift_time":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},{"shift_key":"shift_3","shift_time":{"from":"2021-05-13T10:30:00Z","to":"2021-05-13T12:01:00Z"}}],"actions":[{"order_key":"order_2","demand_key":"demand_3","location_key":"whs","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T10:30:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T10:30:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T10:30:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T10:40:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_2"}]},{"order_key":"order_1","demand_key":"demand_1","location_key":"whs","todolist":[{"job_type":"READY_TO_WORK","job_time":"2021-05-13T10:40:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T10:40:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T10:50:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T10:50:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_1"}]},{"order_key":"order_3","demand_key":"demand_5","location_key":"loc_3","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:00:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:00:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:00:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:10:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:10:00Z"}],"cargo_placements":[]},{"order_key":"order_1","demand_key":"demand_2","location_key":"loc_1","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:18:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:18:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:18:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:28:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:28:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_1"}]},{"order_key":"order_2","demand_key":"demand_4","location_key":"loc_2","todolist":[{"job_type":"LOCATION_ARRIVAL","job_time":"2021-05-13T11:41:00Z"},{"job_type":"READY_TO_WORK","job_time":"2021-05-13T11:41:00Z"},{"job_type":"START_WORK","job_time":"2021-05-13T11:41:00Z"},{"job_type":"FINISH_WORK","job_time":"2021-05-13T11:51:00Z"},{"job_type":"LOCATION_DEPARTURE","job_time":"2021-05-13T11:51:00Z"}],"cargo_placements":[{"box_key":"box01","cargo_key":"cargo_2"}]}],"waitlist":[],"start_location_key":"loc_1","finish_location_key":"loc_1"}],"statistics":{"total_statistics":{"cost":15785.5,"reward":5000,"measurements":{"driving_time":52,"waiting_time":0,"working_time":50,"arriving_time":6,"departure_time":6,"total_time":114,"distance":7743,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},"orders_count":3,"plan_orders_count":3,"waitlist_orders_count":0,"performers_count":1,"capacity_utilization":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"quality":{"soft_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}},"hard_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}}}},"trips_statistics":[{"trip_key":"trip_shift_1","statistics":{"cost":15785.5,"reward":5000,"measurements":{"driving_time":52,"waiting_time":0,"working_time":50,"arriving_time":6,"departure_time":6,"total_time":114,"distance":7743,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T12:10:00Z"}},"orders_count":3,"plan_orders_count":3,"waitlist_orders_count":0,"performers_count":1,"capacity_utilization":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"capacity_max":{"mass":0.02,"volume":0.02,"capacity_x":0.2,"capacity_y":0.2,"capacity_z":0.2},"quality":{"soft_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}},"hard_time_window_violations":{"before":{"keys":[],"count":0},"after":{"keys":[],"count":0}}}},"stop_statistics":[{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":[],"measurements":{"driving_time":0,"waiting_time":0,"working_time":0,"arriving_time":0,"departure_time":1,"total_time":1,"distance":1125,"time_window":{"from":"2021-05-13T10:20:00Z","to":"2021-05-13T10:21:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"location_key":"whs","demand_ids":["order_2#demand_3","order_1#demand_1"],"measurements":{"driving_time":10,"waiting_time":0,"working_time":20,"arriving_time":1,"departure_time":1,"total_time":32,"distance":0,"time_window":{"from":"2021-05-13T10:29:00Z","to":"2021-05-13T10:51:00Z"}},"upload":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}},{"location":{"latitude":55.83022,"longitude":37.623083,"arrival_duration":1,"departure_duration":1},"location_key":"loc_3","demand_ids":["order_3#demand_5"],"measurements":{"driving_time":8,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":20,"distance":1594,"time_window":{"from":"2021-05-13T10:59:00Z","to":"2021-05-13T11:11:00Z"}},"current_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}},{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":["order_1#demand_2"],"measurements":{"driving_time":6,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":18,"distance":764,"time_window":{"from":"2021-05-13T11:17:00Z","to":"2021-05-13T11:29:00Z"}},"download":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}},"current_load":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}}},{"location":{"latitude":55.839876,"longitude":37.629588,"arrival_duration":1,"departure_duration":1},"location_key":"loc_2","demand_ids":["order_2#demand_4"],"measurements":{"driving_time":11,"waiting_time":0,"working_time":10,"arriving_time":1,"departure_time":1,"total_time":23,"distance":1905,"time_window":{"from":"2021-05-13T11:40:00Z","to":"2021-05-13T11:52:00Z"}},"download":{"count":1,"capacity":{"mass":10,"volume":2,"capacity_x":1,"capacity_y":2,"capacity_z":3}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83730739,"longitude":37.62006685,"arrival_duration":1,"departure_duration":1},"location_key":"whs","demand_ids":[],"measurements":{"driving_time":9,"waiting_time":0,"working_time":0,"arriving_time":1,"departure_time":1,"total_time":11,"distance":1230,"time_window":{"from":"2021-05-13T12:00:00Z","to":"2021-05-13T12:02:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}},{"location":{"latitude":55.83079795705435,"longitude":37.62993934276462,"arrival_duration":1,"departure_duration":1},"location_key":"loc_1","demand_ids":[],"measurements":{"driving_time":8,"waiting_time":0,"working_time":0,"arriving_time":1,"departure_time":0,"total_time":9,"distance":1125,"time_window":{"from":"2021-05-13T12:09:00Z","to":"2021-05-13T12:10:00Z"}},"upload":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"download":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}},"current_load":{"count":0,"capacity":{"mass":0,"volume":0,"capacity_x":0,"capacity_y":0,"capacity_z":0}}}],"total_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}},"max_load":{"count":2,"capacity":{"mass":20,"volume":4,"capacity_x":2,"capacity_y":4,"capacity_z":6}}}]},"validations":[],"unplanned_orders":[],"progress":100,"info":{"status":"FINISHED_IN_TIME","result_version":0,"planning_time":0,"waiting_time":0}},
        )

    def testAnalyticsTask(self):
        """Test AnalyticsTask"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
