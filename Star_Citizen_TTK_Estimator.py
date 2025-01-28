# Star Citizen TTK Calculator
import json
from statistics import mean
from pandas import DataFrame

BAL="bal"
ENG="eng"
K=3
RNG_COEF=.5
TRUE_TTK=True
DEBUG=False
defaults = {
        "shield_bal_res": (0.25, 0),
        "shield_eng_res": (0.50, 0),
        "shield_bal_absorb": (.30, 0),
        "shield_eng_absorb": (1, 1)
    }

"""
    Calculator for estimating best case time to kill including factors like shield and hull resistances and absorbtions.
    BE SURE TO PUT POWER SETTINGS TO A VALID SETTING WHEN ENTERING THESE VALUES

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
                        "accuracy": 0,
                        "time_on_target": 0
                    }
                }
    Weapons:
                {
                            "type": BAL | ENG,
                            "sustained_dps": 0,
                            "runtime": 0,
                            "count": 0
                        }
"""
ships = [{
            "name": "Hurricane",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 742.3,
                                "count": 2
                            }
                        ],
                        "accuracy": .5,
                        "time_on_target": .5
                        },
                    "Turret": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 556.6,
                                "count": 4
                            }
                        ],
                        "accuracy": .7,
                        "time_on_target": .8
                        }
                    }
                },
            "vital_hull_name": "Nose",
            "vital_hull_hp": 7000,
            "hull_bal_res": 0.54,
            "hull_eng_res": 0,
            "shield_hp": 6170,
            "shield_faces": 1,
            "pitch_rate": 38
        },{
            "name": "Gladiator",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 735.7,
                                "count": 2
                            }
                        ],
                        "accuracy": .5,
                        "time_on_target": .7
                        },
                    "Turret": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 551.6,
                                "count": 2
                            }
                        ],
                        "accuracy": .7,
                        "time_on_target": .95
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 5500,
            "hull_bal_res": 0.54,
            "hull_eng_res": 0,
            "shield_hp": 6170,
            "shield_faces": 1,
            "pitch_rate": 40
        },{
            "name": "Gladius",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 291,
                                "count": 3
                            }
                        ],
                        "accuracy": .7,
                        "time_on_target": .7
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 2134,
            "hull_bal_res": 0.57,
            "hull_eng_res": 0,
            "shield_hp": 4480,
            "shield_faces": 1,
            "pitch_rate": 70
        },{
            "name": "F7A MKii",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 227.4,
                                "count": 4
                            },
                            {
                                "type": ENG,
                                "sustained_dps": 340.8,
                                "count": 2
                            }
                        ],
                        "accuracy": .4,
                        "time_on_target": .7
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 3000,
            "hull_bal_res": 0.55,
            "hull_eng_res": -0.03,
            "shield_hp": 4480,
            "shield_faces": 1,
            "pitch_rate": 56
        },{
            "name": "F7C-M MKii",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": ENG,
                                    "sustained_dps": 626.3,
                                    "count": 2
                                },
                                {
                                    "type": ENG,
                                    "sustained_dps": 469.6,
                                    "count": 2
                                }
                            ],
                        "accuracy": .6,
                        "time_on_target": .7
                        },
                    "Turret": {
                        "weapons": [
                                {
                                    "type": ENG,
                                    "sustained_dps": 939.2,
                                    "count": 2
                                }
                            ],
                        "accuracy": .7,
                        "time_on_target": .95
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 3150,
            "hull_bal_res": 0.55,
            "hull_eng_res": -.03,
            "shield_hp": 6740,
            "shield_faces": 1,
            "pitch_rate": 52
        },{
            "name": "F7C-M MKii Heartseeker",
            "loadouts": {
                "Stealth": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 509.3,
                                    "runtime": 150,
                                    "count": 2
                                },
                                {
                                    "type": BAL,
                                    "sustained_dps": 844,
                                    "runtime": 150,
                                    "count": 2
                                }
                            ],
                        "accuracy": .5,
                        "time_on_target": .7
                        },
                    "Turret Operator": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 1132.5,
                                    "runtime": 150,
                                    "count": 2
                                }
                            ],
                        "accuracy": .3,
                        "time_on_target": .95
                        }
                    },
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 3150,
            "hull_bal_res": 0.55,
            "hull_eng_res": -.03,
            "shield_hp": 3840,
            "shield_faces": 1,
            "pitch_rate": 52
        },{
            "name": "Redeemer",
            "loadouts": {
                "Mixed": {
                    "Pilot": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 844,
                            "runtime": 100,
                            "count": 2
                        }],
                        "accuracy": .4,
                        "time_on_target": .5
                    },
                    "Top Turret": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 844,
                            "runtime": 100,
                            "count": 2
                        }],
                        "accuracy": .4,
                        "time_on_target": 0.7
                    },
                    "Bottom Turret": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 844,
                            "runtime": 100,
                            "count": 2
                        }],
                        "accuracy": .4,
                        "time_on_target": 0.7
                    },
                    "Chin Turret": {
                        "weapons": [{
                            "type": ENG,
                            "sustained_dps": 291,
                            "runtime": 100,
                            "count": 2
                        }],
                        "accuracy": .4,
                        "time_on_target": 0.4
                    },
                    "Rear Turret": {
                        "weapons": [{
                            "type": ENG,
                            "sustained_dps": 291,
                            "runtime": 100,
                            "count": 2
                        }],
                        "accuracy": .4,
                        "time_on_target": 0.2
                    }
                }
            },
            "shield_hp": 37020,
            "shield_faces": 2,
            "vital_hull_name": "Body",
            "vital_hull_hp": 17000,
            "hull_bal_res": .5,
            "hull_eng_res": 0,
            "pitch_rate": 32
        },{
            "name": "Constellation Andromeda",
            "loadouts": {
                "Mixed": {
                    "Pilot": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 1244.7,
                            "runtime": 120,
                            "count": 4
                        }],
                        "accuracy": .4,
                        "time_on_target": .5
                    },
                    "Top Turret": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 845,
                            "runtime": 120,
                            "count": 2
                        }],
                        "accuracy": .35,
                        "time_on_target": 0.7
                    },
                    "Bottom Turret": {
                        "weapons": [{
                            "type": BAL,
                            "sustained_dps": 845,
                            "runtime": 120,
                            "count": 2
                        }],
                        "accuracy": .35,
                        "time_on_target": 0.7
                    }
                }
            },
            "shield_hp": 60000,
            "shield_faces": 4,
            "vital_hull_name": "Nose",
            "vital_hull_hp": 20000,
            "hull_bal_res": .53,
            "hull_eng_res": 0,
            "pitch_rate": 30
        }]

def calculate_ttk(target, attacker, attacker_pitch_rate, include_modifiers=True):
    # resistance determines how much damage is reduced
    # shield absorbtion determines the ratio of how much damage is passed through to the hull vs applied to shield
    # kill is when hull_hp is zero
    
    if include_modifiers is True:
        estimation = True
    else:
        estimation = False

    # calculate ship advantage rating
    adv = 1
    if estimation is True:
        adv = max([1 + (K*(attacker_pitch_rate - target["pitch_rate"])/100), 0.1])

    # set starting values and init trackers
    hull_hp = target["vital_hull_hp"]
    hull_bal_res = target["hull_bal_res"]
    hull_eng_res = target["hull_eng_res"]
    
    shield_hp = int(target["shield_hp"]/target["shield_faces"])

    shield_bal_res_max, shield_bal_res_min = target.get("shield_bal_res", defaults["shield_bal_res"])
    shield_bal_res_current = shield_bal_res_max
    shield_eng_res_max, shield_eng_res_min = target.get("shield_eng_res", defaults["shield_eng_res"])
    shield_eng_res_current = shield_eng_res_max
    
    shield_bal_absorb_max, shield_bal_absorb_min = target.get("shield_bal_absorb", defaults["shield_bal_absorb"])
    shield_bal_absorb_current = shield_bal_absorb_max
    shield_eng_absorb_max, shield_eng_absorb_min = target.get("shield_eng_absorb", defaults["shield_eng_absorb"])
    shield_eng_absorb_current = shield_eng_absorb_max

    multipliers = {}

    attacking = {}
    starting_dps = {
        "bal": 0,
        "eng": 0
        }
    for key in attacker.keys():
        attacking[key] = {
                f"{ENG}_sustained_dps": 0,
                f"{BAL}_sustained_dps": 0,
                f"{BAL}_runtimes": [],
                f"{BAL}_runtime": 0,
                "accuracy": 1,
                "time_on_target": attacker.get(key, {}).get("time_on_target", 1)
            }

        multipliers[key] = 1

        if estimation is True:
            attacking[key]["accuracy"] = max([0.1, min([ ((attacker.get(key, {}).get("accuracy", 1) - 0.5) * RNG_COEF) + 0.5, 1 ])])
            if key.lower() == "pilot":
                multipliers[key] = attacker[key]["time_on_target"] * adv
            multipliers[key] = multipliers[key]/2
    
        for weapon in attacker[key]["weapons"]:
            attacking[key][f"{weapon['type']}_sustained_dps"] += (weapon["sustained_dps"] * weapon["count"] * multipliers[key])
            if DEBUG:
                print(f'dps added: ({weapon["sustained_dps"]} * {weapon["count"]} * {multipliers[key]})')
            if weapon['type'] == BAL:
                for i in range(weapon['count']):
                    attacking[key][f"{weapon['type']}_runtimes"].append(weapon.get("runtime", 0))

        if len(attacking[key][f"{BAL}_runtimes"]) > 0:
            attacking[key][f'{BAL}_runtime'] = mean(attacking[key][f"{BAL}_runtimes"])

        starting_dps["eng"] += attacking[key][f'{ENG}_sustained_dps']
        starting_dps["bal"] += attacking[key][f'{BAL}_sustained_dps']

    damage_tracking = {
        "shield": {
            BAL: 0,
            ENG: 0
            },
        "hull": {
            BAL: 0,
            ENG: 0
            }
        }

    # start timer and begin damage
    timer = 0
    while hull_hp > 0:
        # for pilot and turrets
        for operator in attacking.keys():
            bal_runtime = attacking[operator]["bal_runtime"]
            bal_sustained_dps = attacking[operator]["bal_sustained_dps"]
            eng_sustained_dps = attacking[operator]["eng_sustained_dps"]
            accuracy = attacking[operator]["accuracy"]
            
            # Calculate Ballistic Damage
            if bal_runtime >= timer:
                if shield_hp > 0:
                    bal_dmg_to_shield = (
                        bal_sustained_dps * (1-shield_bal_res_current)
                        ) * shield_bal_absorb_current
                    
                    bal_dmg_to_hull = (
                                (bal_sustained_dps * accuracy) - bal_dmg_to_shield
                                    ) - (
                                (bal_sustained_dps * accuracy) - bal_dmg_to_shield) * hull_bal_res
                else:
                    bal_dmg_to_hull = bal_sustained_dps - (bal_sustained_dps * accuracy * hull_bal_res)
                    bal_dmg_to_shield = 0
            else:
                bal_dmg_to_hull = 0
                bal_dmg_to_shield = 0

            # Calculate Energy Damage
            if shield_hp > 0:
                eng_dmg_to_shield = (
                    eng_sustained_dps * (1-shield_eng_res_current)
                    ) * shield_eng_absorb_current
                
                eng_dmg_to_hull = (
                    (eng_sustained_dps - eng_dmg_to_shield) * accuracy
                    ) - ((eng_sustained_dps - eng_dmg_to_shield )* accuracy) * hull_eng_res
                
            else:
                eng_dmg_to_hull = eng_sustained_dps - (
                    eng_sustained_dps * accuracy * hull_eng_res
                    )
                
                eng_dmg_to_shield = 0

            # Apply Damage to Target
            shield_hp = shield_hp - (bal_dmg_to_shield + eng_dmg_to_shield)
            hull_hp = hull_hp - (bal_dmg_to_hull + eng_dmg_to_hull)
            
            damage_tracking["shield"][BAL] += bal_dmg_to_shield 
            damage_tracking["shield"][ENG] += eng_dmg_to_shield
            damage_tracking["hull"][BAL] += bal_dmg_to_hull
            damage_tracking["hull"][ENG] += eng_dmg_to_hull

            # Decrement Resistances
            if shield_hp > 0:
                shield_bal_absorb_current = shield_bal_absorb_max - (
                    (shield_bal_absorb_max - shield_bal_absorb_min) * (
                        shield_hp/(
                            target["shield_hp"]/target["shield_faces"]
                            )
                        )
                    )
                shield_eng_absorb_current = shield_eng_absorb_max - (
                    (
                        shield_eng_absorb_max - shield_eng_absorb_min
                        ) * (
                            shield_hp/(
                                target["shield_hp"]/target["shield_faces"]
                                )
                            )
                    )
                shield_bal_res_current = shield_bal_res_max - (
                    (
                        shield_bal_res_max - shield_bal_res_min
                        ) * (
                        shield_hp/(
                            target["shield_hp"]/target["shield_faces"]
                            )
                        )
                    )
                shield_eng_res_current = shield_eng_res_max - (
                    (
                        shield_eng_res_max - shield_eng_res_min
                        ) * (
                        shield_hp/(
                            target["shield_hp"]/target["shield_faces"]
                            )
                        )
                    )
            else:
                shield_bal_absorb_current = 0
                shield_eng_absorb_current = 0
                shield_bal_res_current = 0
                shield_eng_res_current = 0
            
        timer += 1
            
        # Flag for Out of Ammo Looping
        bal_runtimes = [attacking[operator][f"{BAL}_runtime"] for operator in attacking.keys()]
        eng_running = [attacking[operator][f"{ENG}_sustained_dps"] for operator in attacking.keys()]
        if not (0 not in eng_running) and timer >= max(bal_runtimes):
            hull_hp = 0
            timer = 9999999

    bal_remaining = {}

    for operator in attacking.keys():
        if attacking[key][f"{BAL}_runtime"] >= 0:
            if timer >= attacking[key][f"{BAL}_runtime"]:
                bal_remaining[key] = 0
            else:
                bal_remaining[key] = int(100 - (timer / attacking[key][f"{BAL}_runtime"])*100)
    
    if estimation:
        print(f'  Movement Advantage:\t {(int(100*adv)-100)}%')
        print(f'    With Modifiers    ', end = "")
    else:
        print(f'    With No Modifiers ', end = "")         
    if DEBUG is True:
        print("For Ship")
        for key in attacking.keys():
            print(f'\t\t     For {key}')
            print(f'\t\t\tAccuracy:        {int(100*attacking[key]["accuracy"])}%')
            print(f'\t\t\tTime on Target:  {int(100*multipliers[key])}%')
        print(f'\t\tdamage_tracking={json.dumps(damage_tracking, indent=2)}')
        print(f'\t\t{starting_dps=}')
        print(f'\t\t{target["vital_hull_hp"]=} shield_face_hp={target["shield_hp"]/target["shield_faces"]}')
        print(f'\t\tadvantage: 1 + ({K}*({attacker_pitch_rate-target["pitch_rate"]})/100) = {adv}')
        for key in attacking:
            print(f'\t\t    {key}')
            print(f'\t\t\taccuracy: [ 0.1, (({attacking.get(key, {}).get("accuracy", 1)} - 0.5) * {RNG_COEF}) + 0.5, 1 ]')
            print(f'\t\t\ttime on target: [ 0.1, (({attacking.get(key, {}).get("time_on_target", 1)} - .5) / {adv}) + .5, 1 ]')

    
    if timer >= 9999999:
        return "No Kill", 9999999, adv-1
    else:
        return f'{timer} seconds', timer, adv-1

if __name__ == "__main__":
    results = {}
    win_count = {}
    for ship in ships:
        win_count[ship["name"]] = {"count": 0, "wins": ""}
        results[ship["name"]] = {}
        
    for target in ships:
        target_display = f'{target["name"]}\'s {target["vital_hull_name"]}'
        print(f'\nTARGET: {target_display}')
        
        for attacker in ships:
            if target["name"] == attacker["name"] and len(ships) > 1:
                continue
            else:
                for loadout in attacker["loadouts"].keys():
                    print(f'  ATTACKER: {attacker["name"]} with {loadout} loadout VS {target_display}')

                    result, ttk, adv = calculate_ttk(target, attacker["loadouts"][loadout], attacker["pitch_rate"], include_modifiers=True)
                    print(f'      Time to Kill: {result}')

                    if TRUE_TTK:
                        if results[target["name"]].get(attacker["name"], {}).get("ttk", 9999999 + 1) > ttk:
                            results[target["name"]][attacker["name"]] = { "ttk": ttk, "adv": adv }

                    r, t, a = calculate_ttk(target, attacker["loadouts"][loadout], attacker["pitch_rate"], include_modifiers=False)
                    print(f'      Time to Kill: {r}\n')
                    if not TRUE_TTK:
                        if results[target["name"]].get(attacker["name"], {}).get("ttk", 9999999 + 1) > t:
                            results[target["name"]][attacker["name"]] = { "ttk": t, "adv": a }
            
        winner = None
        for i in results[target["name"]]:
            if results[target["name"]][i]["ttk"] <= (results[target["name"]][winner]["ttk"] if winner else results[target["name"]][i]["ttk"]):
                winner = i
        win_count[winner]["count"] += 1
        win_count[winner]["wins"] += f'\t{target_display}'

    print("\tDOGFIGHT RESULTS")
    done = []
    for a in ships:
        for b in ships:
            truncated_name_a = a["name"].split(" ")[-1] if len(a["name"]) > 15 else a["name"]
            truncated_name_b = b["name"].split(" ")[-1] if len(b["name"]) > 15 else b["name"]

            matchup = " vs ".join(sorted([truncated_name_a, truncated_name_b]))

            if matchup in [row[0] for row in done] or a["name"] == b["name"]:
                continue

            else:
                winner = None
                loser = None
                
                a_ttk = results[b["name"]][a["name"]]["ttk"]
                a_adv = results[b["name"]][a["name"]]["adv"]

                b_ttk = results[a["name"]][b["name"]]["ttk"]
                b_adv = results[a["name"]][b["name"]]["adv"]

                if b_ttk < a_ttk:
                    if a_ttk - b_ttk < a_ttk/10:
                        done.append([matchup, 
                                    f' (Tie) {truncated_name_b}', 
                                    b_ttk, 
                                    a_ttk - b_ttk, 
                                    b_adv])
                    else:
                        done.append([matchup, 
                                     truncated_name_b, 
                                     b_ttk, 
                                     a_ttk - b_ttk, 
                                     b_adv])

                elif a_ttk < b_ttk:
                    if b_ttk - a_ttk < b_ttk/10:
                        done.append([matchup,
                                    f' (Tie) {truncated_name_a}',
                                    a_ttk,
                                    b_ttk - a_ttk,
                                    a_adv])
                    else:
                        done.append([matchup,
                                    truncated_name_a,
                                    a_ttk,
                                    b_ttk - a_ttk,
                                    a_adv])

                else:
                    done.append([matchup, "Tie", a_ttk, b_ttk - a_ttk, str((a_adv, b_adv))])

    col = ["Matchup", "Winner", "TTK (s)", "Diff (s)", "Winner's Advantage"]
    df = DataFrame(data=done, columns=col)
    print(df.sort_values(by=col[0]).to_string(
        index=False,
        justify="left",
        formatters={
                col[0]: '{:<30}'.format,
                col[1]: '{:<20}'.format,
                col[2]: '{:<7}'.format,
                col[3]: '{:< 7}'.format,
                col[4]: '{:>.0%}'.format
            }
        ))
