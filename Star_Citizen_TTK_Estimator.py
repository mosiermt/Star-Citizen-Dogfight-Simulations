# Star Citizen TTK Calculator
import json
from statistics import mean
from pandas import DataFrame
import requests
import base64


K=1
RNG_COEF=1.2
TRUE_TTK=True
DEBUG=True
ALLOW_SELF_FIGHTS=True

BAL="bal"
ENG="eng"

defaults = {
        "shield_bal_res": (0.25, 0),
        "shield_eng_res": (0.50, 0),
        "shield_bal_absorb": (.30, 0),
        "shield_eng_absorb": (1, 1)
    }

ships = [{
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
                        "time_on_target": .8
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
                "Revenant and Shredders": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 454,
                                    "runtime": 160,
                                    "count": 4
                                },
                                {
                                    "type": BAL,
                                    "sustained_dps": 844,
                                    "runtime": 150,
                                    "count": 2
                                }
                            ],
                        "accuracy": .45,
                        "time_on_target": .65
                        }
                    },
                "Panther and Rhino": {
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
                        "time_on_target": .8
                        }
                    },
                "Ardor and Attrition": {
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
                                    "count": 4
                                }
                            ],
                        "accuracy": .6,
                        "time_on_target": .55
                        },
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
                "Ardor and Attrition": {
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
                        "time_on_target": .55
                        },
                    "Turret": {
                        "weapons": [
                                {
                                    "type": ENG,
                                    "sustained_dps": 470,
                                    "count": 2
                                }
                            ],
                        "accuracy": .7,
                        "time_on_target": .7
                        }
                    },
                "Panther and Rhino": {
                    "Pilot": {
                        "weapons": [
                            {
                                "type": ENG,
                                "sustained_dps": 227.4,
                                "count": 2
                            },
                            {
                                "type": ENG,
                                "sustained_dps": 340.8,
                                "count": 2
                            }
                        ],
                        "accuracy": .4,
                        "time_on_target": .8
                        },
                    "Turret": {
                        "weapons": [
                                {
                                    "type": ENG,
                                    "sustained_dps": 227,
                                    "count": 2
                                }
                            ],
                        "accuracy": .4,
                        "time_on_target": .9
                        }
                    },
                "Heartseeker and Tigerstrikes": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 422,
                                    "runtime": 128,
                                    "count": 2
                                },
                                {
                                    "type": BAL,
                                    "sustained_dps": 567,
                                    "runtime": 170,
                                    "count": 2
                                }
                            ],
                        "accuracy": .37,
                        "time_on_target": .45
                        },
                    "Turret": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 567,
                                    "runtime": 170,
                                    "count": 2
                                }
                            ],
                        "accuracy": .3,
                        "time_on_target": .6
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 3150,
            "hull_bal_res": 0.55,
            "hull_eng_res": -.03,
            "shield_hp": 6720,
            "shield_faces": 1,
            "pitch_rate": 52
        },{
            "name": "F8C Lightning",
            "loadouts": {
                "Energy": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": ENG,
                                    "sustained_dps": 266,
                                    "count": 4
                                },
                                {
                                    "type": ENG,
                                    "sustained_dps": 160,
                                    "count": 4
                                }
                            ],
                        "accuracy": .4,
                        "time_on_target": .75
                        }
                    },
                "Ballistic": {
                    "Pilot": {
                        "weapons": [
                                {
                                    "type": BAL,
                                    "sustained_dps": 454,
                                    "runtime": 160,
                                    "count": 4
                                },
                                {
                                    "type": BAL,
                                    "sustained_dps": 302,
                                    "runtime": 160,
                                    "count": 4
                                }
                            ],
                        "accuracy": .45,
                        "time_on_target": .5
                        }
                    }
                },
            "vital_hull_name": "Body",
            "vital_hull_hp": 7650,
            "hull_bal_res": 0.55,
            "hull_eng_res": -.03,
            "shield_hp": 12340,
            "shield_faces": 1,
            "pitch_rate": 35
        },{
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
        adv = 1 + (K*(attacker_pitch_rate - target["pitch_rate"])/100)

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
            attacking[key]["accuracy"] = max([0.1, min([ ((attacker.get(key, {}).get("accuracy", 1) - .5) * RNG_COEF) + 0.5, 1 ])])
            if key.lower() == "pilot":
                multipliers[key] = attacker[key]["time_on_target"] * adv
        
        w = 0
        for weapon in attacker[key]["weapons"]:
            w += 1
            attacking[key][f"{weapon['type']}_sustained_dps"] += (weapon["sustained_dps"] * weapon["count"] * multipliers[key])
            if DEBUG and estimation:
                print(f'    {key} Weapon Group {w}: Type - {weapon["type"].upper()} | Raw DPS per Weapon - {int(weapon["sustained_dps"])} | Count - x{weapon["count"]} | Modifier - x{multipliers[key]}')
            
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
        print(f'\n    With Modifiers')
        print(f'        Total Ballistic Sustained DPS: {int(starting_dps["bal"])}')
        print(f'        Total Energy Sustained DPS: {int(starting_dps["eng"])}')
        print(f'        Movement Advantage: {(int(100*adv)-100)}% (Based on turn rates and accelleration compared to target)\n')
        
    else:
        print(f'\n    With No Modifiers')
        print(f'        Total Ballistic Sustained DPS: {int(starting_dps["bal"])} dps')
        print(f'        Total Energy Sustained DPS: {int(starting_dps["eng"])} dps')
        print(f'        Movement Advantage: {(int(100*adv)-100)}% (Based on turn rates and accelleration compared to target)\n')
        
    if DEBUG is True:
        for key in attacking.keys():
            print(f'\tMultipliers Added For {key} Weapons')
            print(f'\t\tTime on Target:  {int(100*multipliers[key])}% (Percent of dps hitting the ship at all)')
            print(f'\t\tAccuracy:        {int(100*attacking[key]["accuracy"])}% (Percent of dps hitting vital vs non-vital hull areas)')
        print(f'\n\tAggregations - ')
        print(f'\t\tTotal Damage Applied to Shields:   Ballistic - {int(damage_tracking["shield"][BAL])} | Energy - {int(damage_tracking["shield"][ENG])}')
        print(f'\t\tTotal Damage Applied to Hull:      Ballistic: {int(damage_tracking["hull"][BAL])} | Energy - {int(damage_tracking["hull"][ENG])}')
        print(f'\t\tHull HP Remaining: {max([0, int(hull_hp)])} of {int(target["vital_hull_hp"])} hp')
        print(f'\t\tShield Face HP Remaining: {max([0, int(shield_hp)])} of {int(target["shield_hp"]/target["shield_faces"])} hp\n')
            
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
            if not ALLOW_SELF_FIGHTS and target["name"] == attacker["name"] and len(ships) > 1:
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
                                    f'{truncated_name_b} (Tie) ', 
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
                                    f'{truncated_name_a} (Tie) ',
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
                    done.append([matchup, "Tie", a_ttk, b_ttk - a_ttk, a_adv])

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
