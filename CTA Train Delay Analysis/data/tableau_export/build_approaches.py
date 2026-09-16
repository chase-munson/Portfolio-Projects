#!/usr/bin/env python3
"""
Collapse CTA Train Tracker poll snapshots into one row per station approach.

Source grain : one row per train per ~60s poll (train_data table)
Output grain : one row per (line, run) continuously approaching one station

Usage:
    python build_approaches.py <source.db> <out.csv> <state_in.pkl|NONE> <state_out.pkl> [--header]

State carries episodes that are still open at the end of a file so an approach
spanning a month boundary is emitted once, not twice.
"""
import csv, os, pickle, re, sqlite3, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

CHI = ZoneInfo("America/Chicago")
GAP = timedelta(minutes=10)      # same run + same station after this long = new approach

LINE_NAME = {"Red":"Red Line","Blue":"Blue Line","Brn":"Brown Line","G":"Green Line",
             "Org":"Orange Line","P":"Purple Line","Pink":"Pink Line","Y":"Yellow Line"}
DIR_LABEL = {1:"North/West bound", 5:"South/East bound"}

COLS = ["episode_id","line","line_name","route_number","train_direction","direction_label",
        "next_station_id","next_station_name",
        "first_seen_local","last_seen_local","service_date","hour_local","day_of_week",
        "final_predicted_arrival","first_eta_min","final_eta_min","eta_slip_min",
        "tracked_min","polls","delayed_polls","ever_delayed","ever_approaching",
        "last_latitude","last_longitude","last_heading","source_month"]


def mins(a, b):
    """Minutes from b to a, rounded to 2dp; None if either is unparseable."""
    if a is None or b is None:
        return None
    return round((a - b).total_seconds() / 60.0, 2)


def parse_local(s):
    """predicted_time / arrival_time are naive local (America/Chicago) ISO strings."""
    try:
        return datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def emit(ep):
    ts0, ts1 = ep["ts_first"], ep["ts_last"]
    l0, l1 = ts0.astimezone(CHI), ts1.astimezone(CHI)
    arr0, arr1 = ep["arr_first"], ep["arr_last"]
    prd1 = ep["prd_last"]
    return {
        "episode_id": f"{ep['line']}-{ep['run']}-{ts0.strftime('%Y%m%dT%H%M%S')}",
        "line": ep["line"],
        "line_name": LINE_NAME.get(ep["line"], ep["line"]),
        "route_number": ep["run"],
        "train_direction": ep["dir"],
        "direction_label": DIR_LABEL.get(ep["dir"], "Unknown"),
        "next_station_id": ep["stn"],
        "next_station_name": ep["stn_name"],
        "first_seen_local": l0.strftime("%Y-%m-%d %H:%M:%S"),
        "last_seen_local": l1.strftime("%Y-%m-%d %H:%M:%S"),
        "service_date": l1.strftime("%Y-%m-%d"),
        "hour_local": l1.hour,
        "day_of_week": l1.strftime("%A"),
        "final_predicted_arrival": arr1.strftime("%Y-%m-%d %H:%M:%S") if arr1 else "",
        "first_eta_min": mins(arr0, ep["prd_first"]),
        "final_eta_min": mins(arr1, prd1),
        "eta_slip_min": mins(arr1, arr0),
        "tracked_min": round((ts1 - ts0).total_seconds() / 60.0, 2),
        "polls": ep["polls"],
        "delayed_polls": ep["delayed"],
        "ever_delayed": 1 if ep["delayed"] else 0,
        "ever_approaching": 1 if ep["approaching"] else 0,
        "last_latitude": ep["lat"],
        "last_longitude": ep["lon"],
        "last_heading": ep["hdg"],
        "source_month": ep["src"],
    }


def main():
    db, out_csv, state_in, state_out = sys.argv[1:5]
    write_header = "--header" in sys.argv
    m = re.search(r"(\d{2})_(\d{4})", os.path.basename(db))
    src = f"{m.group(2)}-{m.group(1)}" if m else os.path.basename(db)

    open_eps = {}
    if state_in != "NONE" and os.path.exists(state_in):
        with open(state_in, "rb") as fh:
            open_eps = pickle.load(fh)

    con = sqlite3.connect("file:" + db + "?mode=ro", uri=True)
    con.execute("pragma cache_size=-200000")
    cur = con.execute(
        "select timestamp,line,route_number,train_direction,next_station_id,"
        "next_station_name,predicted_time,arrival_time,is_approaching,is_delayed,"
        "latitude,longitude,heading from train_data order by rowid")

    mode = "w" if write_header else "a"
    n_in = n_out = 0
    with open(out_csv, mode, newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        if write_header:
            w.writeheader()
        for (ts, line, run, tdir, stn, stn_name, prd, arr,
             appr, dly, lat, lon, hdg) in cur:
            n_in += 1
            t = datetime.fromisoformat(ts)
            key = (line, run)
            ep = open_eps.get(key)
            if ep is not None and (ep["stn"] != stn or ep["dir"] != tdir
                                   or t - ep["ts_last"] > GAP):
                w.writerow(emit(ep)); n_out += 1
                ep = None
            if ep is None:
                ep = {"line": line, "run": run, "dir": tdir, "stn": stn,
                      "stn_name": stn_name, "ts_first": t, "arr_first": parse_local(arr),
                      "prd_first": parse_local(prd), "polls": 0, "delayed": 0,
                      "approaching": 0, "src": src}
                open_eps[key] = ep
            ep["ts_last"] = t
            ep["arr_last"] = parse_local(arr)
            ep["prd_last"] = parse_local(prd)
            ep["polls"] += 1
            ep["delayed"] += 1 if dly else 0
            ep["approaching"] += 1 if appr else 0
            ep["lat"], ep["lon"], ep["hdg"] = lat, lon, hdg

        if state_out == "FLUSH":
            for ep in open_eps.values():
                w.writerow(emit(ep)); n_out += 1
            open_eps = {}

    con.close()
    if state_out not in ("FLUSH", "NONE"):
        with open(state_out, "wb") as fh:
            pickle.dump(open_eps, fh)
    print(f"{src}: read {n_in:,} polls -> wrote {n_out:,} approaches, "
          f"{len(open_eps):,} still open")


if __name__ == "__main__":
    main()
