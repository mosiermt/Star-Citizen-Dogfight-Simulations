# Star-Citizen-Dogfight-Simulations
Based on data provided from sites like spviewer.eu, this simulator takes into account things like ship loadouts and flight performance to make a rough estimation of time to kill for each matchup and compares it to see who is most likely to win

Calculator for estimating best case time to kill including factors like shield and hull resistances and absorbtions.
    BE SURE TO PUT POWER SETTINGS TO A VALID SETTING WHEN ENTERING THESE VALUES

VALUE DESCRIPTIONS:
Accuracy
         - This field is just 1 - the value given by spviewer for the weapons spread.  This does not work for shotguns yet
         - Accuracy uses the spread value to determine what percentage of the rounds that hit the target will deal damage to the vital hull component
         - The Range Coefficient (RNG_COEF) is a modifier to normalize that accuracy percentage based on standard dogfighting ranges

Time on Target
         - This field is a 0 to 1 representation of how proficient the operator is with that weapon group.
         - It represents the amount of time firing the weapon where the rounds actually hit the target ship.
         - Take into account things like barrel spin up time when making this estimate.
         - The value 0.7 (70%) felt the most realistic to me for a pilot and 0.9 (90%) for a turret gunner with a great view
         - For turrets with opposing view areas, where only one can fire at a time, use half of their normal Time on Target.

Pitch Rate
         - Pitch Rate is used to give a rough approximation of the ships agility.
         - When simulating the fight, each ships agility is compared in order to give an advantage to the ship with more maneuverability
         - This advantage is used to reduce the overall average sustained dps in order to simulate a longer time to kill against a fast moving opponent


TEMPLATES:
    Ship
        {
            "name": "",
            "loadouts": {},
            "shield_hp": 0,
            "shield_faces": 0,
            "vital_hull_name": "",
            "vital_hull_hp": 0,
            "hull_bal_res": 0,
            "hull_eng_res": 0,
            "pitch_rate": 0
        }
    Loadouts:
    LOADOUT_NAME: {
                    OPERATOR: {
                        "weapons": [],
                        "accuracy": 0, # 1 - spread value found in Weapon Details This will be the percentage of shots that deal damage to the vital hull component at super close range
                        "time_on_target": 0 # rough estimate of what percentage rounds actually hit the target while firing
                    }
                }
    Weapons:
                {
                            "type": BAL | ENG,
                            "sustained_dps": 0,
                            "runtime": 0,
                            "count": 0
                        }
