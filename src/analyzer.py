import sklearn
import datetime
import pandas as pd
import numpy as np
import scipy

class TestSubject():

    def __init__(
        self,
        name : str,
        tested_from : datetime.datetime,
        tested_till : datetime.datetime,
        item_name : str,
        item_x : float,
        item_y : float
    ) -> None:
        self.name = name
        self.tested_from = tested_from
        self.tested_till = tested_till

        self.item_name = item_name
        self.item_x = item_x
        self.item_y = item_y


    def to_string(self) -> str:
        
        start_string = self.tested_from.strftime("%Y/%m/%d %H:%M:%S")
        end_string   = self.tested_till.strftime("%Y/%m/%d %H:%M:%S")
        text = f"{self.name}:\nTest Period : {start_string} ~ {end_string}\nTarget Item : {self.item_name}\n Located At : {self.item_x}, {self.item_y}"
        return text


class Analyzer():

    def __init__(
        self,
        test_subjects : list,

        raw_sales_result : pd.DataFrame,
        raw_loc_result : pd.DataFrame,
        raw_face_result : pd.DataFrame
    
    ) -> None:
        self.test_subjects = test_subjects
        
        ## List of PANDAS
        self.sales_results = self._split_sales_according_to_test_subject(raw_test_results= raw_sales_result)
        self.loc_results = self._split_loc_according_to_test_subject(raw_test_results= raw_loc_result)
        self.face_results = self._split_face_according_to_test_subject(raw_test_results= raw_face_result)
        
        ## DATA for Actual 
        self.time_spent  = self._from_loc_results_get_time_spent_results(self.loc_results)
        self.visit_count = self._from_loc_results_get_visit_results(self.loc_results)
        

    def _from_loc_results_get_visit_results(
        self,
        loc_results : list
    ) -> list:
        visit_count = []

        visit_count.append(len(loc_results[0]['user_id'].unique()))
        visit_count.append(len(loc_results[1]['user_id'].unique()))

        print(visit_count)
        return visit_count


    def _from_loc_results_get_time_spent_results(
        self,
        loc_results : list
    ) -> list:

        ## Assuming every result has time window of 5 seconds

        def is_near(
            row : pd.Series,
            test_subject : TestSubject
        ):
            distance = np.sqrt(np.square((test_subject.item_x - row['x'])) + np.square((test_subject.item_y - row['y'])))
            if distance < 0.5 :
                return True

            else :
                return False

        time_spent_results = []

        for index, loc_result in enumerate(loc_results):
            time_spent_result = {}
            for _, row in loc_result.iterrows():
                user_id = row['user_id']
                if user_id not in time_spent_result:
                    time_spent_result[user_id] = {
                        "user_id" : user_id,
                        "time_spent" : 0
                    }
                    
                if is_near(row, self.test_subjects[index]) :
                    time_spent_result[user_id]["time_spent"] = time_spent_result[user_id]["time_spent"] + 5
            
            print(len(time_spent_result))    
            time_spent_results.append(pd.DataFrame.from_dict(time_spent_result, orient="index").reset_index())

        ## USER | TIME_SPENT (NEAR_ITEM)
        ##   1  | 123
        ##   2  | 4331
        ##   4  | 543
        #time_spent_results = pd.DataFrame(time_spent_results)
        
        print(time_spent_results[0].head(5))
        print(time_spent_results[1].head(5))
        
        return time_spent_results


    def _split_result_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame,
        date_column_name :str
    ) -> list:

        test_results = []

        def distinguish_by_time(row):
            current_date = row[date_column_name]
            name = ""
            for test_subject in self.test_subjects:
                name = ""
                if current_date >= test_subject.tested_from and current_date <= test_subject.tested_till :
                    name =  test_subject.name
                    break
            
            return name

        raw_test_results['name'] = raw_test_results.apply(lambda x : distinguish_by_time(x), axis = 1)
        
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[0].name])
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[1].name])

        return test_results


    def _split_sales_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame
    ) -> list:

        test_results = []
        date_column_name = "date"

        def distinguish_by_time(row):
            current_date = str(row[date_column_name])
            current_year  = int(current_date[:4])
            current_month = int(current_date[4:6])
            current_day  = int(current_date[6:8])

            current_date = datetime.datetime(year=current_year, month=current_month, day = current_day)

            name = ""
            for test_subject in self.test_subjects:
                name = ""
                if current_date >= test_subject.tested_from and current_date < test_subject.tested_till :
                    name =  test_subject.name
                    break
            
            return name

        raw_test_results['name'] = raw_test_results.apply(lambda x : distinguish_by_time(x), axis = 1)
        
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[0].name])
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[1].name])
        
        print(test_results)
        return test_results


    def _split_loc_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame
    ) -> list:

        test_results = []
        date_column_name = "date"
        time_column_name = "time"

        def distinguish_by_time(row):
            current_date = str(int(row[date_column_name]))
            
            current_year  = int(current_date[:4])
            current_month = int(current_date[4:6])
            current_day  = int(current_date[6:8])

            current_time = str(int(row[time_column_name]))
            current_hour = int(current_time[:2])
            current_min = int(current_time[2:4])
            current_sec = int(current_time[4:6])

            current_datetime = datetime.datetime(
                year=current_year,
                month=current_month,
                day = current_day,
                hour = current_hour,
                minute =current_min,
                second = current_sec
            )

            name = ""
            for test_subject in self.test_subjects:
                name = ""
                if current_datetime >= test_subject.tested_from and current_datetime < test_subject.tested_till :
                    name =  test_subject.name
                    break
            
            return name

        raw_test_results['name'] = raw_test_results.apply(lambda x : distinguish_by_time(x), axis = 1)
        
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[0].name])
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[1].name])
        
        print(test_results[0].head(5))
        print(test_results[1].head(5))
        return test_results


    def _split_face_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame
    ) -> list:

        test_results = []
        date_column_name = "date"
        time_column_name = "time"

        def distinguish_by_time(row):
            current_date = str(int(row[date_column_name]))
            
            current_year  = int(current_date[:4])
            current_month = int(current_date[4:6])
            current_day  = int(current_date[6:8])

            current_time = str(int(row[time_column_name]))
            current_hour = int(current_time[:len(current_time)-4])
            current_min = int(current_time[len(current_time)-4:len(current_time)-2])
            current_sec = int(current_time[len(current_time)-2:len(current_time)])

            current_datetime = datetime.datetime(
                year=current_year,
                month=current_month,
                day = current_day,
                hour = current_hour,
                minute =current_min,
                second = current_sec
            )

            name = ""
            for test_subject in self.test_subjects:
                name = ""
                if current_datetime >= test_subject.tested_from and current_datetime < test_subject.tested_till :
                    name =  test_subject.name
                    break
            
            return name

        raw_test_results['name'] = raw_test_results.apply(lambda x : distinguish_by_time(x), axis = 1)
        
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[0].name])
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[1].name])
        
        print(test_results[0].head(5),test_results[1].head(5))
        return test_results


    def do_reject_null_hypothesis(
        self,
        p_value : float,
        threshold : float = 0.005
    ) -> bool:

        if p_value < threshold:
            ## Reject the Null Hypothesis
            return True
        
        else :
            ## Failed to Reject the Null Hypothesis
            return False


    def _get_z_score(
        self,
        x : float,
        mean : float,
        std : float
    ) -> float:
        return (x- mean) /std


    def _z_score_two_distribution(
        self,
        n_control : int,
        n_variant : int,
        mean_control: float,
        mean_variant : float,
        var_control : float,
        var_variant : float
    ) -> float:
        s_mean = mean_variant - mean_control
        s_var = (var_control/n_control) + (var_variant/n_variant)

        z_score = s_mean / np.sqrt(s_var)

        return z_score


    def p_value_from_z(
        self,
        z_score : float
    ):
        #p_value_1_tail = scipy.stats.norm.sf(z_score)
        p_value_2_tail = scipy.stats.norm.sf(abs(z_score))

        return p_value_2_tail


    def sale_analysis(self):

        distributions = []

        for idx, df_sales in enumerate(self.sales_results):
            distribution = {}
            distribution['n'] = self.visit_count[idx]
            sales_data = np.array(df_sales['count'].values.tolist())

            distribution['mean'] = float(np.mean(sales_data))
            distribution['var']  = float(np.var(sales_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value

        
    def time_spent_analysis(self):
        
        distributions = []

        for idx, df_time_spent in enumerate(self.time_spent):
            distribution = {}
            distribution['n'] = self.visit_count[idx]
            time_spent_data = np.array(df_time_spent['time_spent'].values.tolist())

            distribution['mean'] = float(np.mean(time_spent_data))
            distribution['var']  = float(np.var(time_spent_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value
    

    def face_count_analysis(self):

        distributions = []

        for idx, df_face in enumerate(self.face_results):
            distribution = {}
            distribution['n'] = self.visit_count[idx]
            sales_data = np.array(df_face['facecount'].values.tolist())

            distribution['mean'] = float(np.mean(sales_data))
            distribution['var']  = float(np.var(sales_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value

            

        
        
