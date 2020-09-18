import json
class ParseJson():
    def get_jsonvalue(self,content,node):
        pass

    def update_jsonvalue(self,wholejson,casestatus):
        for keyitem in casestatus.keys():
            wholejson[keyitem] = casestatus[keyitem]
        return  wholejson

if __name__=="__main__":
    jsonvalue={"power_on_time_value": 0,
                  "mode": "cool",
                  "power_off_time_value": 0,
                  "wind_swing_ud": "off",
                  "dry": "off",
                  "eco": "off",
                  "purifier": "off",
                  "error_code": 10,
                  "power_on_timer": "off",
                  "comfort_power_save": "off",
                  "prevent_cold": "off",
                  "small_temperature": 0,
                  "power_off_timer": "off",
                  "kick_quilt": "off",
                  "power": "off",
                  "version": 39,
                  "wind_swing_lr": "off",
                  "ptc": "off",
                  "temperature": 17,
                  "wind_speed": 102,
                  "strong_wind": "off"
                }
    a=ParseJson().update_jsonvalue(jsonvalue,{"power": "on","pow11":"2222"})
    print(a)


