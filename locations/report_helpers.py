#!/usr/bin/env python

# from pymongo import Connection
from django.conf import settings
from pymongo import MongoClient
from bson import json_util
import logging
import time


client = MongoClient(settings.MONGO_URL)
adminDb = client['admin']
adminDb.authenticate("root","beetroot");

db=client[settings.MONGO_DB]
# client = MongoClient(settings.MONGO_HOST)
# db=client[settings.MONGO_DB]
# db.authenticate(settings.MONGO_DB, settings.MONGO_PW)

logger = logging.getLogger('django')


def get_hvac_report(key, id, start_ts, end_ts):
  #TODO: concatenate all activity items into one long list of strings
  # print(key, id, start_ts, end_ts)
  adminDb = client['admin']
  adminDb.authenticate("root","beetroot");
  logger.debug('get_hvac_report : %s, %s, %s,  %s', key, id, start_ts, end_ts)
  reduce_fun = """
    function(o, p) {
      p.count++;
      p.on += o.on;
      print(o+" : "+p);
      if (o.g_on != undefined) {
        p.g_count++;
        p.g_total += o.g_on;
      }
      if (o.fc_on != undefined) {
        p.fc_count++;
        p.fc_total += o.fc_on;
      }
      if (o.y1_on != undefined) {
        p.y1_count++;
        p.y1_total += o.y1_on;
        p.has_cool = true;
      }
      if (o.y2_on != undefined) {
        p.y2_count++;
        p.y2_total += o.y2_on;
      }
      if (o.y3_on != undefined) {
        p.y3_count++;
        p.y3_total += o.y3_on;
      }
      if (o.mix_on != undefined) {
        p.mix_count++;
        p.mix_total += o.mix_on;
      }
      if (o.w1_on != undefined) {
        p.w1_count++;
        p.w1_total += o.w1_on;
        p.has_heat = true;
      }
      if (o.w2_on != undefined) {
        p.w2_count++;
        p.w2_total += o.w2_on;
      }
      if (o.h_on != undefined) {
        p.h_count++;
        p.h_total += o.h_on;
      }

      if (p.has_cool) {
        p.c_sp += o.c_sp_avg;

        if (o.supply_c_avg != undefined) {
          p.supply_c_count++;
          p.supply_c_total += o.supply_c_avg;
        }

        if (o.perf_c_avg != undefined) {
          p.perf_c_count++;
          p.perf_c_total += o.perf_c_avg;
        }
      }

      if (p.has_heat) {
        p.h_sp += o.h_sp_avg;

        if (o.supply_h_avg != undefined) {
          p.supply_h_count++;
          p.supply_h_total += o.supply_h_avg;
        }

        if (o.perf_h_avg != undefined) {
          p.perf_h_count++;
          p.perf_h_total += o.perf_h_avg;
        }
      }

    }
  """

  finalize_fun = """
    function(p) {
      j = {};
      j.on = p.on/p.count;
      if (p.g_count > 0) j.g_on = p.g_total/p.g_count;
      if (p.fc_count > 0) j.fc_on = p.fc_total/p.fc_count;
      if (p.y1_count > 0) j.y1_on = p.y1_total/p.y1_count;
      if (p.y2_count > 0) j.y2_on = p.y2_total/p.y2_count;
      if (p.y3_count > 0) j.y3_on = p.y3_total/p.y3_count;
      if (p.w1_count > 0) j.w1_on = p.w1_total/p.w1_count;
      if (p.w2_count > 0) j.w2_on = p.w2_total/p.w2_count;
      if (p.h_count > 0) j.h_on = p.h_total/p.h_count;

      j.fc_total = p.fc_total;
      j.mix_total = p.mix_total;
      j.y1_total = p.y1_total;
      j.y2_total = p.y2_total;

      if (p.has_cool) {
        j.c_sp = p.c_sp/p.count;

        if (p.supply_c_count > 0) {
          j.supply_c = p.supply_c_total/p.supply_c_count;
        }

        if (p.perf_c_count > 0) {
          j.perf_c = p.perf_c_total/p.perf_c_count;
        }
      }

      if (p.has_heat) {
        j.h_sp = p.h_sp/p.count;

        if (p.supply_h_count > 0) {
          j.supply_h = p.supply_h_total/p.supply_h_count;
        }

        if (p.perf_h_count > 0) {
          j.perf_h = p.perf_h_total/p.perf_h_count;
        }
      }

      return j;

    }
  """

  out = db.daily_logs.group(
    {},
    {
      'key':key,
      'controller_id':id,
      'ts':{'$gte':start_ts, '$lte':end_ts}
    },
    {
      'count':0, 'on':0,
      'c_sp':0,
      'h_sp':0,
      'perf_c_count':0, 'perf_c_total':0,
      'perf_h_count':0, 'perf_h_total':0,
      'supply_h_count':0, 'supply_h_total':0,
      'supply_c_count':0, 'supply_c_total':0,
      'g_count':0, 'g_total':0,
      'y1_count':0, 'y1_total':0,
      'y2_count':0, 'y2_total':0,
      'y3_count':0, 'y3_total':0,
      'w1_count':0, 'w1_total':0,
      'w2_count':0, 'w2_total':0,
      'fc_count':0, 'fc_total':0,
      'mix_count':0, 'mix_total':0
    },
    reduce_fun,
    finalize_fun
  )
  logger.debug('get_hvac_report  out : %s', out)

  if len(out) > 0:
    return out[0]
  else:
    return None


def get_light_report(key, id, start_ts, end_ts):
  reduce_fun = """
    function(o, p) {
      p.count++;
      p.on += o.on;
      if (o.scheduled_on != undefined) {
        p.scheduled_on += o.scheduled_on;
      }
      if (o.avg != undefined) {
        p.avg_count++;
        p.avg_total += o.avg;
      }
    }
  """

  finalize_fun = """
    function(p) {
      p.total = p.on;
      p.on = p.on/p.count;
      if (p.avg_total > 0) {
        p.avg = p.avg_total/p.avg_count;
      }
    }
  """

  out = db.daily_logs.group(
    {},
    {
      'key':key,
      'controller_id':id,
      'ts':{'$gte':start_ts, '$lte':end_ts}
    },
    {
      'count':0, 'on':0, 'scheduled_on':0, 'total':0, 'avg_total':0, 'avg_count':0
    },
    reduce_fun,
    finalize_fun
  )

  if len(out) > 0:
    return out[0]
  else:
    return None


def get_kw_report(key, id, start_ts, end_ts):


  reduce_fun = """
    function(o, p) {
      p.count++;

      p.d_total += o.demand_avg;
      p.total += o.total;

      var d = o.ts.getDay();
      p.day_totals[d] += o.total;
      p.day_counts[d] += 1;

      if (p.min == undefined || o.demand_min < p.min) {
        p.min = o.demand_min;
      }

      if (o.demand_max > p.peak) {
        p.peak = o.demand_max;
      }

    }
  """

  finalize_fun = """
    function(p) {
      j = {};

      j.count = p.count;
      j.avg = p.d_total/p.count;
      j.davg = p.total/p.count;
      j.total = p.total;
      j.min = p.min;
      j.peak = p.peak;

      j.day_avgs = [-1,-1,-1,-1,-1,-1,-1];
      for (var i=0;i<7;i++) {
        if (p.day_counts[i] > 0) {
          j.day_avgs[i] = p.day_totals[i] / p.day_counts[i];
        }
      }

      return j;
    }
  """

  search = {
    'key':key,
    'ts':{'$gte':start_ts, '$lte':end_ts}
  }

  if id == 'demand analyzer':
    search['type'] = id
  else:
    search['controller_id'] = id

  out = db.daily_logs.group(
    {},
    search,
    {
      'count':0,
      'd_total':0,
      'total':0,
      'peak':0,
      'day_totals':[0,0,0,0,0,0,0],
      'day_counts':[0,0,0,0,0,0,0]
    },
    reduce_fun,
    finalize_fun
  )

  if len(out) > 0:
    return out[0]
  else:
    return None


# def temp_daily_kw_totals_helper(timething):


def get_daily_kw_totals(key, start_ts, end_ts):
  totals = list(db.daily_logs.find({'key':key,
                               'controller_id':'demand analyzer',
                              'ts':{'$gte':start_ts, '$lte':end_ts}},
                              ['ts', 'total']))
  print(totals)
  return [

    # {'time':time.mktime(t['ts'].timetuple()), 'value':t['total']}
    {'time':str(t['ts']).split()[0], 'value':t['total']}
    for t in totals
  ]
