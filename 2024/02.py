import math
file = "02_data.txt"
safeReport = 0
safeReportTolerance = 0

def report_safety(report, tolerance=0)->bool:
  signe = math.copysign(1, report[0] - report[1])
  if signe == 0:
    return False
  for i in range(len(report)-1):
    diff = report[i] - report[i+1]
    level_sign = math.copysign(1, diff)
    if level_sign != signe:
      return False
    if abs(diff) < 1 or abs(diff) > 3:
      return False
  return True


with open(file, "r") as reports:
  for report in reports:
    # ELs nivells estan separats per espais
    report = report.split(" ")
    # Convertim els nivells a enters
    report = [int(x) for x in report]
    if report_safety(report):
      safeReport += 1
      safeReportTolerance += 1
    else:
      for i in range(len(report)):
        newReport = report[:i] + report[i+1:]
        if report_safety(newReport):
          safeReportTolerance += 1
          break

print("Reports valids que hi ha:", safeReport) #202
print("Reports valids amb tolerència:", safeReportTolerance) #271