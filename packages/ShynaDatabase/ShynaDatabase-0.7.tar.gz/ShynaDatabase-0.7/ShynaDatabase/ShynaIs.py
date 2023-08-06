from haversine import haversine
from ShynaProcess import ShynaWeather
from ShynaDatabase import Shdatabase
from Shynatime import ShTime


class ShynaIs:
    """
    Is_Shivam table is created for now but not connected
    Looking out for below details to crosscheck the environment health
    For Mobile:
    1)  is_location_received_from_primary_mobile?
    2)  is_this_is_the_first_alarm?
    3)  is_shivam_moving?
    4)  is_mobile_device_offline?
    5)  is_shivam_at_home?
    6)  is_shivam_in_front_of_any_cam?
    7)  is_there_alarm_to_set?
    8)  is_shivam_working_for_more_than_4_hour?
    9)  is_shivam_working_for_more_than_6_hour?
    10) is_shivam_working_for_more_than_8_hour?
    11) is_this_is_first_time_on_cam?
    12) is_shivam_working_late_night?
    13) is_shivam_dead?
    14) is_shivam_walking?
    15) is_PC_online?
    16) is_mob_online?
    17) is_rasp_online?

    For now if the data is received, we are good, if not then create a task for rasp to speak where the data is not received.
    ==========================================================================================================================
    Future Plan
    1) is_cam_online?
    2) is_shivam_driving
    3) Is there anything shivam should be aware about
    4) Is last bill costly then last one
    5) Is Shivam watching movies?
    6) Is there item in buying list
    7) Is there a buying list
    8) Is_there_clutter_data
    """
    result = []
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    s_process_ws = ShynaWeather.ShynaWeather()
    is_this = False

    def is_location_received_from_primary_mobile(self):
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='location_check' "
            self.result = self.s_data.select_from_table()
            for result in self.result:
                for item in result:
                    task_time_sequence.append(item)
            time_diff = self.s_time.string_to_time_with_date(
                self.s_time.now_time) - self.s_time.string_to_time_with_date(time_string=str(task_time_sequence[0]))
            print(time_diff)
            if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date("00:01:30"):
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_this_is_the_first_alarm(self, received_time):
        """Will check first thing in the morning. No repetition
        Added filter for alarm in task manager but will need for reminder as well for overall understanding
        """
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.query = "SELECT task_time FROM Task_Manager where (task_date='" + str(self.s_time.now_date) + "') and (task_type='alarm')"
            self.result = self.s_data.select_from_table()
            if "Empty" in self.result:
                self.is_this = False
            else:
                self.is_this = True
                for result in self.result:
                    for item in result:
                        task_time_sequence.append(item)
                task_time_sequence = sorted(task_time_sequence)
                if self.s_time.string_to_time_with_date(task_time_sequence[0]) >= self.s_time.string_to_time_with_date(
                        str(received_time)):
                    self.is_this = True
                else:
                    self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_moving(self):
        self.is_this = False
        speed_list = []
        distance = []
        response = []
        try:
            self.s_data.query = "SELECT shivam_speed FROM shivam_device_location order by count DESC limit 13"
            self.result = self.s_data.select_from_table()
            for row in self.result:
                speed_list.append(row[0])
            # print(speed_list)
            for i in range(len(speed_list) - 1):
                if float(speed_list[i]) < 0.01:
                    response.append(False)
                else:
                    response.append(True)
            my_dict = {i: response.count(i) for i in response}
            maximum = max(my_dict, key=my_dict.get)
            # print(my_dict, maximum)
            self.is_this = str(maximum)
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_at_home(self):
        self.is_this = False
        latitude_list = []
        longitude_list = []
        distance = []
        try:
            self.s_data.query = "SELECT new_latitude, new_longitude FROM shivam_device_location order by count DESC limit 3"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                latitude_list.append(item[0])
                longitude_list.append(item[1])
            self.s_data.query = "SELECT latitude, longitude FROM shivam_standard_location_long_lat where loc_name='home_gzb';"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                distance_from_one = haversine(point1=(float(latitude_list[0]), float(longitude_list[0])), point2=(float(item[0]), float(item[1])))
                if distance_from_one <= 0.09:
                    distance.append(True)
                else:
                    distance.append(False)
            my_dict = {i: distance.count(i) for i in distance}
            self.is_this = max(my_dict, key=my_dict.get)
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_in_front_of_any_cam(self):
        self.is_this = False
        face_time_list = []
        response = []
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date='" + \
                                str(self.s_time.now_date) + "' order by count DESC limit 5"
            self.result = self.s_data.select_from_table()
            if "Empty" in self.result:
                self.is_this = False
            else:
                for face_time in self.result:
                    time_diff = self.s_time.string_to_time_with_date(
                        self.s_time.now_time) - self.s_time.string_to_time_with_date(face_time[0])
                    face_time_list.append(str(time_diff))
                face_time_list = sorted(face_time_list)
                for item in face_time_list:
                    if self.s_time.string_to_time_with_date(item) < self.s_time.string_to_time_with_date("00:10:00"):
                        response.append(True)
                    else:
                        response.append(False)
                my_dict = {i: response.count(i) for i in response}
                if int(my_dict.get(True)) == 5:
                    self.is_this = True
                else:
                    self.is_this = False
        except Exception as e:
            print(e)
            self.is_this = False
        finally:
            return self.is_this

    def is_there_alarm_to_set(self):
        self.is_this = False
        try:
            self.s_data.query = "SELECT count,alarm_time,repeat_frequency FROM alarm where alarm_date='" \
                                + str(self.s_time.now_date) + "' and alarm_status = 'TRUE'"
            alarm = self.s_data.select_from_table()
            for row in alarm:
                count = row[0]
                alarm_time = row[1]
                repeat_frequency = row[2]
                print(count, alarm_time, repeat_frequency)
                if self.s_time.task_in_next_hour(task_time=alarm_time) is True:
                    self.s_data.query = "INSERT INTO Task_Manager (new_date, new_time, task_id, task_date, task_time, " \
                                        "task_type, Speak, snooze_status, snooze_duration, task_status) VALUES ('" \
                                        + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" \
                                        + str(count) + "', '" + str(self.s_time.now_date) + "', '" + str(alarm_time) + \
                                        "', 'alarm', 'wake up Shivam', 'True', '15', 'running');"
                    self.s_data.create_insert_update_or_delete()
                    if str(repeat_frequency).lower().__eq__('daily'):
                        new_date = self.s_time.daily()
                        self.s_data.query = "UPDATE alarm SET alarm_date = '" + str(new_date) + "' WHERE (`count` = '" \
                                            + str(count) + "');"
                        self.s_data.create_insert_update_or_delete()
                        self.is_this = True
                    elif str(repeat_frequency).lower().__eq__('weekends'):
                        new_date = self.s_time.weekends()
                        self.s_data.query = "UPDATE alarm SET alarm_date = '" + str(new_date) + "' WHERE (`count` = '" \
                                            + str(count) + "');"
                        self.s_data.create_insert_update_or_delete()
                        self.is_this = True
                    elif str(repeat_frequency).lower().__eq__('weekdays'):
                        new_date = self.s_time.get_weekdays()
                        self.s_data.query = "UPDATE alarm SET alarm_date = '" + str(new_date) + "' WHERE (`count` = '" \
                                            + str(count) + "');"
                        self.s_data.create_insert_update_or_delete()
                        self.is_this = True
                    elif str(repeat_frequency).lower().__eq__('alternative'):
                        new_date = self.s_time.alternative()
                        self.s_data.query = "UPDATE alarm SET alarm_date = '" + str(new_date) + "' WHERE (`count` = '" \
                                            + str(count) + "');"
                        self.s_data.create_insert_update_or_delete()
                        self.is_this = True
                    else:
                        self.s_data.query = "delete from alarm where count='" + str(count) + "'"
                        self.s_data.create_insert_update_or_delete()
                else:
                    print("No upcoming alarm")
        except Exception as e:
            print(e)
            self.is_this = False
        finally:
            return self.is_this

    def is_shivam_working_for_more_than_4_hour(self):
        self.is_this = False
        time_list = []
        res_res = []
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + \
                                str(self.s_time.now_date) + "' order by count DESC limit 480"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                time_list.append(item[0])
            time_list = sorted(time_list, reverse=True)
            # print(time_list)
            for i in range(len(time_list) - 1):
                time_diff = self.s_time.string_to_time_with_date(time_list[i]) - self.s_time.string_to_time_with_date(
                    time_list[i + 1])
                if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date(
                        "00:10:00"):
                    res_res.append(True)
                    self.is_this = True
                elif self.s_time.string_to_time_with_date(str(time_diff)) >= self.s_time.string_to_time_with_date(
                        "00:20:00"):
                    res_res.append(False)
                    res_res.append(False)
                    res_res.append(False)
                    self.is_this = False
                    break
                else:
                    res_res.append(False)
                    self.is_this = False
            my_dict = {i: res_res.count(i) for i in res_res}
            # print(my_dict)
            if int(my_dict.get(True)) >= 478:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_working_for_more_than_6_hour(self):
        self.is_this = False
        time_list = []
        res_res = []
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + str(self.s_time.now_date) + \
                                "' order by count DESC limit 720"
            self.result = self.s_data.create_insert_update_or_delete()
            for item in self.result:
                time_list.append(item[0])
            time_list = sorted(time_list, reverse=True)
            for i in range(len(time_list) - 1):
                time_diff = self.s_time.string_to_time_with_date(time_list[i]) - self.s_time.string_to_time_with_date(
                    time_list[i + 1])
                if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date(
                        "00:10:00"):
                    res_res.append(True)
                    self.is_this = True
                elif self.s_time.string_to_time_with_date(str(time_diff)) >= self.s_time.string_to_time_with_date(
                        "00:20:00"):
                    res_res.append(False)
                    res_res.append(False)
                    res_res.append(False)
                    self.is_this = False
                    break
                else:
                    res_res.append(False)
                    self.is_this = False
            my_dict = {i: res_res.count(i) for i in res_res}
            if int(my_dict.get(True)) >= 718:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_working_for_more_than_8_hour(self):
        self.is_this = False
        time_list = []
        res_res = []
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + str(self.s_time.now_date) + \
                                "' order by count DESC limit 960"
            self.result = self.s_data.create_insert_update_or_delete()
            for item in self.result:
                time_list.append(item[0])
            time_list = sorted(time_list, reverse=True)
            for i in range(len(time_list) - 1):
                time_diff = self.s_time.string_to_time_with_date(time_list[i]) - self.s_time.string_to_time_with_date(
                    time_list[i + 1])
                if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date(
                        "00:10:00"):
                    res_res.append(True)
                    self.is_this = True
                elif self.s_time.string_to_time_with_date(str(time_diff)) >= self.s_time.string_to_time_with_date(
                        "00:30:00"):
                    res_res.append(False)
                    res_res.append(False)
                    res_res.append(False)
                    cmd = "speak: Welcome back Shivam"
                    self.s_data.query = "INSERT INTO shyna_rasp (task_date, task_time, command_to_run) " \
                                        "VALUES('" + str(self.s_time.now_date) + "', '" \
                                        + str(self.s_time.now_time) + "', '" + str(cmd) + "')"
                    self.s_data.create_insert_update_or_delete()
                    self.is_this = False
                    break
                else:
                    res_res.append(False)
                    self.is_this = False
            my_dict = {i: res_res.count(i) for i in res_res}
            if int(my_dict.get(True)) >= 958:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_this_is_first_time_on_cam(self):
        self.is_this = False
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + str(self.s_time.now_date) + \
                                "' order by count ASC limit 1"
            self.result = self.s_data.create_insert_update_or_delete()
            if "Empty" in self.result or "E" in self.result:
                pass
            else:
                for item in self.result:
                    time_diff = self.s_time.string_to_time_with_date(
                        self.s_time.now_time) - self.s_time.string_to_time_with_date(item[0])
                    if self.s_time.string_to_time_with_date(time_diff) <= self.s_time.string_to_time_with_date(
                            "00:0:59"):
                        self.is_this = True
                        cmd = self.s_process_ws.get_weather_sentence()
                        if cmd is False:
                            cmd = "speak: Hello Shiv!"
                        else:
                            cmd = "speak: Hello Shiv! " + str(cmd)
                        self.s_data.query = "INSERT INTO shyna_rasp (task_date, task_time, command_to_run) VALUES('" \
                                            + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + "', '" \
                                            + str(cmd) + "')"
                        self.s_data.create_insert_update_or_delete()
                    else:
                        self.is_this = False
        except Exception as e:
            print(e)
            self.is_this = False
        finally:
            return self.is_this

    def is_shivam_working_late_night(self):
        self.is_this = False
        try:
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + str(self.s_time.now_date) + \
                                "' order by count DESC limit 1"
            self.result = self.s_data.create_insert_update_or_delete()
            if "Empty" in self.result or "E" in self.result:
                self.is_this = False
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_time_with_date("22:00:00") < self.s_time.string_to_time_with_date(
                            str(item[0])) or self.s_time.string_to_time_with_date(
                            str(item[0])) < self.s_time.string_to_time_with_date("04:55:00"):
                        self.is_this = True
                        print(item[0])
                    else:
                        self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_dead(self):
        self.is_this = False
        stat = []
        try:
            stat.append(self.is_location_received_from_primary_mobile())
            stat.append(self.is_shivam_at_home())
            stat.append(self.is_shivam_in_front_of_any_cam())
            stat.append(self.is_shivam_moving())
            stat.append(self.is_shivam_working_for_more_than_4_hour())
            stat.append(self.is_shivam_working_for_more_than_6_hour())
            stat.append(self.is_shivam_working_for_more_than_8_hour())
            if True in stat:
                self.is_this = False
            else:
                self.is_this = True
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_shivam_walking(self):
        self.is_this = False
        speed = [True, False]
        try:
            is_location_received_from_primary_mobile = self.is_location_received_from_primary_mobile()
            if is_location_received_from_primary_mobile is True:
                self.s_data.query = "SELECT shivam_distance_from_previous FROM shivam_device_location ORDER BY count limit DESC"
                self.result = self.s_data.select_from_table()
                for item in self.result:
                    if 1.0 < float(item[0]) < 3.0:
                        speed.append(True)
                    else:
                        speed.append(False)
            my_dict = {i: speed.count(i) for i in speed}
            if int(my_dict.get(True)) >= 478:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_termux_device_online(self):
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='connection_check' "
            self.result = self.s_data.select_from_table()
            for result in self.result:
                for item in result:
                    task_time_sequence.append(item)
            time_diff = self.s_time.string_to_time_with_date(
                self.s_time.now_time) - self.s_time.string_to_time_with_date(time_string=str(task_time_sequence[0]))
            print(time_diff)
            if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date("00:01:30"):
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_pc_device_online(self):
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='pc_online_check' "
            self.result = self.s_data.select_from_table()
            for result in self.result:
                for item in result:
                    task_time_sequence.append(item)
            time_diff = self.s_time.string_to_time_with_date(
                self.s_time.now_time) - self.s_time.string_to_time_with_date(time_string=str(task_time_sequence[0]))
            print(time_diff)
            if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date("00:01:30"):
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this

    def is_rasp_device_online(self):
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='rasp_online_check' "
            self.result = self.s_data.select_from_table()
            for result in self.result:
                for item in result:
                    task_time_sequence.append(item)
            time_diff = self.s_time.string_to_time_with_date(
                self.s_time.now_time) - self.s_time.string_to_time_with_date(time_string=str(task_time_sequence[0]))
            print(time_diff)
            if self.s_time.string_to_time_with_date(str(time_diff)) <= self.s_time.string_to_time_with_date("00:01:30"):
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            return self.is_this


test = ShynaIs()
print(test.is_there_alarm_to_set())