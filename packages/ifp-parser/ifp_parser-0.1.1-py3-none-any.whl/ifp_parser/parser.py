from pathlib import Path
from typing import Dict, List, Optional, Tuple

from lark import Lark, Transformer, v_args

import ifp_parser.icao_standards

package_path = Path(__file__).parent


@v_args(inline=True)
class MessageTransformer(Transformer):
    # TODO: Transformers to breakout full strings for equip etc..

    @v_args(inline=False)
    def start(self, children):
        return list(children)

    def message(self, aftn, plan):
        plan_consolidated = {}

        # Add the message type as a field.
        plan_consolidated["type"] = plan.data.upper()

        # Compile all the fields into a coherent dictionary object.
        for child in plan.children:
            plan_consolidated.update(child)

        return aftn, plan_consolidated

    def aftn_data(self, priority, recipients, dtg, sender):
        # TODO: Smart parser for DTG. Probably compare DTG day to the DOF.
        return {
            "priority": str(priority),
            "recipients": [str(x) for x in recipients.children],
            "sender": str(sender),
        }

    def field_7(self, callsign):
        return {"callsign": str(callsign)}

    def field_8(self, flight_rules, flight_type):
        return {"flight_rules": str(flight_rules), "flight_type": str(flight_type)}

    def field_9(self, aircraft_num, aircraft_type, wake_turbulence):
        return {
            "aircraft_num": aircraft_num and int(aircraft_num) or 1,
            "aircraft_type": str(aircraft_type),
            "wake_turbulence": str(wake_turbulence),
        }

    def field_10(self, equipment, surveillance_equipment):
        equipment = str(equipment)
        equipment_list = []

        for k, v in ifp_parser.icao_standards.EQUIPMENT.items():
            if k in equipment:
                equipment_list.append(v)

        return {
            "equipment": equipment_list,
            "surveillance_equipment": str(surveillance_equipment),
        }

    def field_13(self, icao, time):
        return {
            "departure": {
                "icao": str(icao),
                "time": str(time),
            }
        }

    def field_15(self, speed, altitude, route):
        return {"speed": speed, "altitude": str(altitude), "route": route}

    def field_16(self, icao, time, alternatives):
        return {
            "destination": {
                "icao": str(icao),
                "elapsed_time": str(time),
                "icao_alternatives": alternatives,
            }
        }

    @v_args(inline=False)
    def field_18(self, fields):
        data = []
        for field in fields:
            (field_type, value) = field
            data.append((field_type, value))
        return dict(data)

    def supplemental_data(self, k, v):
        k = str(k)
        v = str(v)
        return k, v

    @v_args(inline=False)
    def route(self, points):
        return points

    def SPEED(self, s: str):
        # Convert to km/h
        scale = {"K": 1, "N": 1.852, "M": 1193.256}
        unit = s[0]
        num = int(s[1:])
        return round(num * scale[unit], 1)


def get_parser():
    return Lark.open(
        package_path / "grammars/fpl.lark",
        rel_to=__file__,
        parser="lalr",
        transformer=MessageTransformer(),
    )


PARSER = get_parser()


def parse(text: str) -> List[Tuple[Optional[Dict], Dict]]:
    return PARSER.parse(text)
