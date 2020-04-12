from django import template

register = template.Library()

@register.filter(name='format_minutes')
def format_minutes(value):
  if value > 60:
    return "%.1f hours" % (value/60.0)
  else:
    return "%.1f minutes" % value

@register.filter(name='format_alarm_code')
def format_alarm_code(c):
  return c.replace("_", " ").upper()

@register.filter(name='format_seconds')    
def format_seconds(value):
  if value:
    if value > 3600:
      return "%.1f hours" % (value/3600.0)
    elif value > 60:
      return "%.1f minutes" % (value/60.0)
    else:
      return "%.1f seconds" % value
  else:
    return '--'

def get_perf_rating(value):
  if value > 60*60:
    return 0
  elif value > 11*60:
    return 1
  elif value > 8*60:
    return 2
  elif value > 4*60:
    return 3
  else:
    return 4

@register.filter(name='perf_pct')
def get_perf_pct(value):
  if value != "":
    inc = 100 * 0.043478
    m = 25 * inc
    mins = float(value)/60.0
    return int(max(0, min(100, m - (mins*inc))))
  else: return 0

@register.filter(name='perf_chart')
def perf_chart(value, cname):
  pct = max(0, get_perf_pct(value))
  num = int(round(float(pct)/10))  
  return "<span class=\"%s\">%s</span><span class=\"reportgray\">%s</span>" % (cname, "/"*num, "/"*(10-num))
  



