from common import *
import matplotlib.pyplot as plt


aggregate_metrics = {
    'benchmark_application': [],

    'l1vcache-read-hit': [],
    'l1vcache-read-miss': [],
    'l1vcache-read-mshr-hit': [],
    'l1vcache-write-hit': [],
    'l1vcache-write-miss': [],
    'l1vcache-write-mshr-hit': [],

    'l2vcache-read-hit': [],
    'l2vcache-read-miss': [],
    'l2vcache-read-mshr-hit': [],
    'l2vcache-write-hit': [],
    'l2vcache-write-miss': [],
    'l2vcache-write-mshr-hit': [],

    'l1vtlb-hit': [],
    'l1vtlb-miss': [],
    'l1vtlb-mshr-hit' : [],

    'l2vtlb-hit': [],
    'l2vtlb-miss': [],
    'l2vtlb-mshr-hit' : []
}

for benchmark_application in benchmark_applications:
    application_path = os.path.join(samples_directory, benchmark_application)
    os.chdir(application_path)
    metrics_file_path = os.path.join(application_path, "metrics.csv")
    
    if not os.path.exists(metrics_file_path):
        print(f"metrics.csv didn't exist for {benchmark_application}, so we're skipping it")
        continue

    metrics_df = pd.read_csv(metrics_file_path)

    # Strip whitespaces from column names and ensure 'value' column is numeric
    metrics_df.columns = metrics_df.columns.str.strip()
    metrics_df['value'] = pd.to_numeric(metrics_df['value'], errors='coerce')

    # Strip whitespaces in 'where' and 'what' columns
    metrics_df['where'] = metrics_df['where'].str.strip()
    metrics_df['what'] = metrics_df['what'].str.strip()

    # metric calculation for l1vcache
    filtered_df_l1vcache = metrics_df[metrics_df['where'].str.contains('L1VCache', na=False)]
    cum_l1vcache_read_hit = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'read-hit', 'value'].sum()
    cum_l1vcache_read_miss = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'read-miss', 'value'].sum()
    cum_l1vcache_read_mshr_hit = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'read-mshr-hit', 'value'].sum()
    cum_l1vcache_write_hit = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'write-hit', 'value'].sum()
    cum_l1vcache_write_miss = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'write-miss', 'value'].sum()
    cum_l1vcache_write_mshr_hit = filtered_df_l1vcache.loc[filtered_df_l1vcache['what'] == 'write-mshr-hit', 'value'].sum()

    # metric calculation for l2vcache
    filtered_df_l2vcache = metrics_df[metrics_df['where'].str.contains('L2', na=False)]
    cum_l2vcache_read_hit = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'read-hit', 'value'].sum()
    cum_l2vcache_read_miss = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'read-miss', 'value'].sum()
    cum_l2vcache_read_mshr_hit = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'read-mshr-hit', 'value'].sum()
    cum_l2vcache_write_hit = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'write-hit', 'value'].sum()
    cum_l2vcache_write_miss = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'write-miss', 'value'].sum()
    cum_l2vcache_write_mshr_hit = filtered_df_l2vcache.loc[filtered_df_l2vcache['what'] == 'write-mshr-hit', 'value'].sum()

    # metric calculation for l1vtlb
    filtered_df_l1vtlb = metrics_df[metrics_df['where'].str.contains('L1VTLB', na=False)]
    cum_l1vtlb_hit = filtered_df_l1vtlb.loc[filtered_df_l1vtlb['what'] == 'hit', 'value'].sum()
    cum_l1vtlb_miss = filtered_df_l1vtlb.loc[filtered_df_l1vtlb['what'] == 'miss', 'value'].sum()
    cum_l1vtlb_mshr_hit = filtered_df_l1vtlb.loc[filtered_df_l1vtlb['what'] == 'mshr-hit', 'value'].sum()

    # metric calculation for l2vtlb
    filtered_df_l2vtlb = metrics_df[metrics_df['where'].str.contains('L2VTLB', na=False)]
    cum_l2vtlb_hit = filtered_df_l2vtlb.loc[filtered_df_l2vtlb['what'] == 'hit', 'value'].sum()
    cum_l2vtlb_miss = filtered_df_l2vtlb.loc[filtered_df_l2vtlb['what'] == 'miss', 'value'].sum()
    cum_l2vtlb_mshr_hit = filtered_df_l2vtlb.loc[filtered_df_l2vtlb['what'] == 'mshr-hit', 'value'].sum()

    # store the metrics for this application
    aggregate_metrics['benchmark_application'].append(benchmark_application)

    aggregate_metrics['l1vcache-read-hit'].append(cum_l1vcache_read_hit)
    aggregate_metrics['l1vcache-read-miss'].append(cum_l1vcache_read_miss)
    aggregate_metrics['l1vcache-read-mshr-hit'].append(cum_l1vcache_read_mshr_hit)
    aggregate_metrics['l1vcache-write-hit'].append(cum_l1vcache_write_hit)
    aggregate_metrics['l1vcache-write-miss'].append(cum_l1vcache_write_miss)
    aggregate_metrics['l1vcache-write-mshr-hit'].append(cum_l1vcache_write_mshr_hit)

    aggregate_metrics['l2vcache-read-hit'].append(cum_l2vcache_read_hit)
    aggregate_metrics['l2vcache-read-miss'].append(cum_l2vcache_read_miss)
    aggregate_metrics['l2vcache-read-mshr-hit'].append(cum_l2vcache_read_mshr_hit)
    aggregate_metrics['l2vcache-write-hit'].append(cum_l2vcache_write_hit)
    aggregate_metrics['l2vcache-write-miss'].append(cum_l2vcache_write_miss)
    aggregate_metrics['l2vcache-write-mshr-hit'].append(cum_l2vcache_write_mshr_hit)

    aggregate_metrics['l1vtlb-hit'].append(cum_l1vtlb_hit)
    aggregate_metrics['l1vtlb-miss'].append(cum_l1vtlb_miss)
    aggregate_metrics['l1vtlb-mshr-hit'].append(cum_l1vtlb_mshr_hit)

    aggregate_metrics['l2vtlb-hit'].append(cum_l2vtlb_hit)
    aggregate_metrics['l2vtlb-miss'].append(cum_l2vtlb_miss)
    aggregate_metrics['l2vtlb-mshr-hit'].append(cum_l2vtlb_mshr_hit)


# metrics to plot
metrics = ['l1vcache-read-hit', 'l1vcache-read-miss', 'l1vcache-read-mshr-hit', 
           'l1vcache-write-hit', 'l1vcache-write-miss', 'l1vcache-write-mshr-hit',
           'l2vcache-read-hit', 'l2vcache-read-miss', 'l2vcache-read-mshr-hit', 
           'l2vcache-write-hit', 'l2vcache-write-miss', 'l2vcache-write-mshr-hit',
           'l1vtlb-hit', 'l1vtlb-miss', 'l1vtlb-mshr-hit',
           'l2vtlb-hit', 'l2vtlb-miss', 'l2vtlb-mshr-hit']

x = range(len(aggregate_metrics['benchmark_application']))

for metric in metrics:
    plt.figure(figsize=(12, 6))
    values = aggregate_metrics[metric]
    plt.bar(x, values, color='green', label=metric)
    plt.title(f'{metric} across all Applications')
    plt.xlabel('Benchmark application')
    plt.ylabel(f'Cumulative {metric} value')
    plt.xticks(x, aggregate_metrics['benchmark_application'], rotation=45)
    plt.tight_layout()
    
    plot_path = os.path.join(samples_directory, f"{metric}.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"Combined visualization saved as {plot_path}")
