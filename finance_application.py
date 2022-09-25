import tkinter as tk
from dbmanager import *
from plots import *
from markowitz import * 

# Setup foundation for GUI and switching frames. 
class PortfolioApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Portfolio Manager")
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='icon.png'))

        self.frames = {}
        for F in (StartPage, CreatePortfolio, AccessPortfolio, AnalyzeStock, 
        CreatePortfolio_withStocks, CreatePortfolio_withRiskPreference, 
        ModifyPortfolio, CreatePortfolioReport):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# Setup start page. 
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home")
        label.pack(side="top", fill="x", pady=10)

        # Create navigation buttons. 
        create_button = tk.Button(self, text="Create Portfolio",
                            command=lambda: controller.show_frame("CreatePortfolio"))
        access_button = tk.Button(self, text="Access Portfolio",
                            command=lambda: controller.show_frame("AccessPortfolio"))
        analyze_button = tk.Button(self, text="Analyze Stock",
                    command=lambda: controller.show_frame("AnalyzeStock"))
        quit_button = tk.Button(self, text="Quit",
            command=quit)
        
        # Put buttons on grid. 
        create_button.pack()
        access_button.pack()
        analyze_button.pack()
        quit_button.pack(side=tk.BOTTOM)


# Setup portfolio creation overview. 
class CreatePortfolio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please Select")
        label.pack(side="top", fill="x", pady=10)

        # Setup navigation buttons. 
        create_stocks = tk.Button(self, text="Create Portfolio with Stocks",
                    command=lambda: controller.show_frame("CreatePortfolio_withStocks"))
        create_risk = tk.Button(self, text="Create Random Portfolio with Risk Preference",
                    command=lambda: controller.show_frame("CreatePortfolio_withRiskPreference"))
        return_button = tk.Button(self, text="Go to the start page",
                    command=lambda: controller.show_frame("StartPage"))
        
        # Put buttons on grid. 
        create_stocks.pack()
        create_risk.pack()
        return_button.pack(side=tk.BOTTOM)


# Setup portfolio creation with stocks. 
class CreatePortfolio_withStocks(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please enter four stock tickers")
        label.pack(side="top", fill="x", pady=10)
        
        # Define function to create portfolio for stocks. 
        def createportfolio(): 
            try: 
                stocks = [stock1.get(), stock2.get(), stock3.get(), stock4.get()]
                markowitz_output = get_weights(stocks)
                add_portfolio(markowitz_output)
                outcomelabel = tk.Label(self, text="Successfully created portfolio.")
                outcomelabel.pack() 
            except: 
                outcomelabel = tk.Label(self, text="Error occured. Please enter four valid stock tickers.")
                outcomelabel.pack()  

        
        # Setup labels and user entry. 
        label1 = tk.Label(self, text="Stock #1")
        label1.pack()    
        stock1 = tk.Entry(self)
        stock1.pack()

        label2 = tk.Label(self, text="Stock #2")
        label2.pack()     
        stock2 = tk.Entry(self)
        stock2.pack()

        label3 = tk.Label(self, text="Stock #3")
        label3.pack()     
        stock3 = tk.Entry(self)
        stock3.pack()

        label4 = tk.Label(self, text="Stock #4")
        label4.pack()     
        stock4 = tk.Entry(self)
        stock4.pack()

        # Create buttons and put on grid. 
        create_store_button = tk.Button(self, text="Create Portfolio",
                            command=createportfolio)
        create_store_button.pack()
        return_button = tk.Button(self, text="Go back.",
                           command=lambda: controller.show_frame("CreatePortfolio"))
        return_button.pack(side=tk.BOTTOM)

# Setup portfolio creation with risk preference. 
class CreatePortfolio_withRiskPreference(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Setup labels and user entry. 
        label = tk.Label(self, text="Please enter your Risk Preference in Decimal")
        label.pack(side="top", fill="x", pady=10)
        label1 = tk.Label(self, text="Risk Preference")
        label1.pack()     
        riskpreference = tk.Entry(self)
        riskpreference.pack()

        # Setup function to create portfolio.
        def create_from_risk_preference(): 
            riskpref = riskpreference.get()
            try: 
                markowitz_output = get_stocks_given_risk_tolerance(float(riskpref))
                add_portfolio(markowitz_output)
                outcomelabel = tk.Label(self, text="Successfully Created Portfolio")
                outcomelabel.pack()  
            except: 
                outcomelabel = tk.Label(self, text="No portfolio found for risk preference. Please try again or increase risk preference.")
                outcomelabel.pack()  

        
        # Setup buttons and put on grid. 
        create_button = tk.Button(self, text="Create Portfolio",
                            command=create_from_risk_preference)
        create_button.pack()

        return_button = tk.Button(self, text="Go back.",
                           command=lambda: controller.show_frame("CreatePortfolio"))
        return_button.pack(side=tk.BOTTOM)


# Setup portfolio access overview. 
class AccessPortfolio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Setup labels and buttons .
        label = tk.Label(self, text="Please Select")
        label.pack(side="top", fill="x", pady=10)
        create_button = tk.Button(self, text="Create Portfolio Report", 
        command=lambda: controller.show_frame("CreatePortfolioReport"))
        create_button.pack()
        modify_button = tk.Button(self, text="Modify Portfolio", 
        command=lambda: controller.show_frame("ModifyPortfolio"))
        modify_button.pack()
        return_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        return_button.pack(side=tk.BOTTOM)


# Setup portfolio reporting overview. 
class CreatePortfolioReport(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select Portfolio")
        label.pack(side="top", fill="x", pady=10)

        # Get all available portfolios. 
        portfolios = get_portfolios()
        
        # Function to create report. 
        def create_report():
            create_portfolio_report(selected.get())
            outcomelabel = tk.Label(self, text="Successfully Exported Report.")
            outcomelabel.pack()  

        # Create options menue.  
        selected = tk.StringVar(self)
        selected.set(portfolios[0])
        portfolio_list = tk.OptionMenu(self, selected, *portfolios)
        portfolio_list.pack()

        # Create buttons and put on grid. 
        report_button = tk.Button(self, text="Create Report", command = create_report)
        report_button.pack()
        return_button = tk.Button(self, text="Go back",
                           command=lambda: controller.show_frame("AccessPortfolio"))
        return_button.pack(side=tk.BOTTOM)


# Setup portfolio modification. 
class ModifyPortfolio(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Setup user entries and labels. 
        portfolio = tk.Label(self, text="Select Portfolio")
        portfolio.pack(side="top", fill="x", pady=10)
        entered_portfolio = tk.Entry(self)
        entered_portfolio.pack()
        ticker = tk.Label(self, text="Enter Ticker")
        ticker.pack(side="top", fill="x", pady=10)
        entered_ticker = tk.Entry(self)
        entered_ticker.pack()
       
       # Create functions to delete and add stocks. 
        def delete():
            try: 
                ticker = entered_ticker.get()
                portfolioId = entered_portfolio.get()
                delete_stock(portfolioId, ticker)
                old_stocks = get_stocks(portfolioId)
                stocks = get_weights(old_stocks)
                creation_date = get_creation_date(portfolioId)
                delete_portfolio(portfolioId)
                update_portfolio(stocks, portfolioId, creation_date)
                outcomelabel = tk.Label(self, text="Successfully deleted stock.")
                outcomelabel.pack()  
            except: 
                outcomelabel = tk.Label(self, text="Error: Please make sure stock ticker is valid and in the selected portfolio.")
                outcomelabel.pack()  

        def add():
            try: 
                ticker = entered_ticker.get()
                portfolioId = entered_portfolio.get()
                stocks = get_stocks(entered_portfolio.get())
                stocks.append(ticker)
                creation_date = get_creation_date(portfolioId)
                new_stocks = get_weights(stocks)
                delete_portfolio(portfolioId)
                update_portfolio(new_stocks, portfolioId, creation_date)
                outcomelabel = tk.Label(self, text="Successfully added stock.")
                outcomelabel.pack()  
            except: 
                outcomelabel = tk.Label(self, text="Error: Please make sure portfolio and stock ticker are valid.")
                outcomelabel.pack()  

        # Setup buttons and put on grid. 
        delete_button = tk.Button(self, text="Delete Stock",
                            command=delete)
        delete_button.pack()
        add_button = tk.Button(self, text="Add Stock",
                            command=add)
        add_button.pack()
        return_button = tk.Button(self, text="Go back.",
                           command=lambda: controller.show_frame("AccessPortfolio"))
        return_button.pack(side=tk.BOTTOM)


# Setup stock analysis. 
class AnalyzeStock(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Setup labels and user input. 
        label = tk.Label(self, text="Enter Stock Ticker")
        label.pack(side="top", fill="x", pady=10)

        # Function to trigger stock report. 
        def create_report():
            try: 
                create_stock_report(ticker.get())
                outcomelabel = tk.Label(self, text="Successfully exported Report.")
                outcomelabel.pack()  
            except: 
                outcomelabel = tk.Label(self, text="Error: Please enter a valid stock ticker.")
                outcomelabel.pack()  

        # Get user entries. 
        ticker = tk.Entry(self, )
        ticker.pack()
        
        #Setup buttons. 
        perform_button = tk.Button(self, text = "Create Report", command = create_report)
        perform_button.pack()
        return_button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        return_button.pack(side=tk.BOTTOM)

if __name__ == "__main__":
    app = PortfolioApp()
    app.mainloop()