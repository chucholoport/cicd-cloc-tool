from utils import *

class Formatter:
    '''
    Creates an object for interpretting cloc diff report (format author: AlDanial)
    '''
    def __init__(self, file:os.path, fig:os.path):
        # declare object variables
        self.rows = ['same','modified','added','removed']
        self.cols = ['files','blank','comment','code']
        # fetch input values
        self.file = file
        self.fig  = fig
        # run object methods
        self.fetch_data()
        self.plot_data()
        self.create_report()
        
    def fetch_data(self):
        '''
        Fetch data from input cloc diff report
        '''
        try:
            print_log(f'fetching data from {self.file}')
            # fetch data into lists
            content = [re.sub(r'same|added|modified|removed|\s+',' ',line).strip() for line in open(self.file, mode='r') if not re.search(r'--+|Language|files|blank|comment|code',line)]
            langs   = list(filter(lambda x: not re.search(r'\d+ \d+ \d+ \d+', x), content))
            values  = [x.split() for x in filter(lambda x: re.search(r'\d+ \d+ \d+ \d+', x), content)]
            # organize data into dataframe
            self.index = pd.MultiIndex.from_product([langs, self.rows],names=['Languange','Category'])
            self.data  = pd.DataFrame(data=values, index=self.index, columns=self.cols)
            self.data  = self.data.astype(int)
            # show output
            logging.debug(f'\n{self.data.to_string()}')
            print_log(f'done.\n')
        except:
            self.index = None
            self.data  = pd.DataFrame()
            print_log(f'unable to fetch data from {self.file}\n')
            
    def plot_data(self):
        '''
        Plot data from input cloc diff report
        '''
        try:
            print_log(f'plotting data from {self.file}')
            # create plot
            self.plot = sns.catplot(
                # plot data
                data=self.data,
                x='Category',
                y='code',
                col=self.data.index.get_level_values(0),
                # plot format
                kind='bar',
                height=4, 
                aspect=.8
            )
            # rename subplots
            self.plot.set_titles("{col_name}")
            # set labels
            self.plot.set_xticklabels(self.rows)
            self.plot.set_xlabels('')
            self.plot.set_ylabels('lines of code')
            # save image
            self.plot.figure.savefig(self.fig)
            print_log(f'done.\n')
        except:
            self.plot = None
            print_log(f'unable to plot data from {self.file}\n')
            logging.exception('')
    
    def create_report(self):
        try:
            print_log(f'creating report from {self.file}')
            # create body
            self.report = bs('<html><body></body></html>').html.body
            # append title
            self.report.append(bs(f'<h1>cicd-cloc-tool</h1>'))
            self.report.append(bs(f'<p>based on <a href="https://github.com/AlDanial/cloc?tab=readme-ov-file#differences-">AlDanial diff-report</a></p>'))
            self.report.append(bs(f'<p>author: <a href="https://www.linkedin.com/in/jesus-salvador-lopez-ortega/">{application.author}</a></p>'))
            self.report.append(bs(f'<p>file processed: {self.file}</p>'))
            # append report
            self.report.append(bs(f'<h3>report details</h3>'))
            self.report.append(bs(self.data.to_html()))
            # append plot figure
            encoded = fig_to_base64(self.plot.figure)
            self.report.append(bs(f'<h3>lines of code plots</h3>'))
            self.report.append(bs('<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))))
            # pretiffy content
            self.report = self.report.prettify()
            print_log(f'done.\n')
        except:
            self.report = None
            print_log(f'unable to create report from {self.file}\n')
            logging.exception('')