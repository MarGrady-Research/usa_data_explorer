
# Import packages
import pandas as pd

# Import data
all_states = pd.read_parquet("data/all_states.parquet")

# convert numbers to numeric
numeric_cols = ['StudentGroup_TotalTested', 'AvgScaleScore', 'ProficientOrAbove_count', 'ProficientOrAbove_percent']
for col in numeric_cols:
    all_states[col] = pd.to_numeric(all_states[col], errors='coerce')

# select only needed columns for district percentiles
selected_columns = ['StateAbbrev', 'SchYear', 'DataLevel', 'DistName', 'NCESDistrictID', 
                   'AssmtName', 'AssmtType', 'Subject', 'GradeLevel', 'StudentGroup_TotalTested',
                   'AvgScaleScore', 'ProficientOrAbove_count', 'ProficientOrAbove_percent', 'ParticipationRate',
                   'DistType', 'DistCharter', 'CountyName','CountyCode']

analysis = all_states[selected_columns]

# select needed rows
analysis = analysis[(analysis['DataLevel'] == 'District') &
                    (analysis['Subject'] != 'sci')]

# create percentiles by state, school year, subject, gradelevel

# define grouping columns
group_cols = ['StateAbbrev', 'SchYear', 'Subject', 'GradeLevel']

# PERCENTILE BASED ON SCALED SCORE

# calculate the rank within each group
analysis['rank_ss'] = (
    analysis.groupby(group_cols)['AvgScaleScore']
    .rank(method = 'min', ascending = True)
    .astype('Int64')
)

# calculate the count of each group
analysis['count_ss'] = (
    analysis.groupby(group_cols)['AvgScaleScore']
    .transform('count')
)

# calculate percentile, ranging from 0 to 100 (or below 100 if ties at the top)
analysis['pctl_ss'] = ((analysis['rank_ss'] - 1) / (analysis['count_ss'] - 1) * 100).round(1)

# PERCENTILE BASED ON PERCENT PROFICIENT

# calculate the rank within each group
analysis['rank_pp'] = (
    analysis.groupby(group_cols)['ProficientOrAbove_percent']
    .rank(method = 'min', ascending = True)
    .astype('Int64')
)

# calculate the count of each group
analysis['count_pp'] = (
    analysis.groupby(group_cols)['ProficientOrAbove_percent']
    .transform('count')
)

# calculate percentile, ranging from 0 to 100 (or below 100 if ties at the top)
analysis['pctl_pp'] = ((analysis['rank_pp'] - 1) / (analysis['count_pp'] - 1) * 100).round(1)

# clean up variables to be snake_case instead of camelCase
column_mapping = {
    'StateAbbrev': 'state_abbrev',
    'SchYear': 'sch_year',
    'DataLevel': 'data_level',
    'DistName': 'dist_name',
    'NCESDistrictID': 'nces_district_id',
    'AssmtName': 'assmt_name',
    'AssmtType': 'assmt_type',
    'Subject': 'subject',
    'GradeLevel': 'grade_level',
    'StudentGroup_TotalTested': 'student_group_total_tested',
    'AvgScaleScore': 'avg_scale_score',
    'ProficientOrAbove_count': 'proficient_or_above_count',
    'ProficientOrAbove_percent': 'proficient_or_above_percent',
    'ParticipationRate': 'participation_rate',
    'DistType': 'dist_type',
    'DistCharter': 'dist_charter',
    'CountyName': 'county_name',
    'CountyCode': 'county_code'
}

# apply new names to analysis dataframe
analysis.rename(columns=column_mapping, inplace=True)

# Save data locally
analysis.to_parquet('data/test_percentiles.parquet', index=False)

