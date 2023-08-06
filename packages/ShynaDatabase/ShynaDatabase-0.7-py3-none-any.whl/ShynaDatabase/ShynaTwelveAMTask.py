from ShynaDatabase import UpdateDistance, ShynaClearHistory


class RunAtTwelve:
    clear_history = ShynaClearHistory.ClearHistory()
    update_distance = UpdateDistance.UpdateDistanceSpeed()

    def at_twelve(self):
        try:
            self.clear_history.clear_data()
            self.update_distance.update_distance_with_haversine()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    RunAtTwelve().at_twelve()


