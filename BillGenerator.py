import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

def main():
    df = pd.read_csv("CompanyDetails.csv")
    df = df.dropna()
    ExistingCompany = df["Company Name"].to_list()
    ExistingCompanyAdd = df["Address"].to_list()
    ExistingCompany.append("Other")
    # Title bar
    st.markdown(
        """<h3 style='text-align: center; color: white; background-color: maroon; padding: 10px;'>Tilak Raj Tour & Travel</h3>
        <h6 style='text-align: center; color: white; background-color: maroon; padding: 10px;'>Add:Noida,U.P. 201301, Contact: 9711981687,8368200227</h3>""",
        unsafe_allow_html=True
    )

    # Layout for UI components
    col1, col2, col3 = st.columns([2, 2, 2])
    # First Column: Dropdowns and Input
    with col1:
        CompanyName = st.selectbox("**Choose Company**",ExistingCompany, key="dropdown1")
        if CompanyName == "Other":
            with st.form(key='**Company Details**'):
                name = st.text_input("Enter Company Name")
                Address = st.text_input("Enter Company Address")
                submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Display a confirmation dialog
                save_confirmation = st.radio(
                    "Do you want to save your details?",
                    ("Yes", "No")
                )
    
                if save_confirmation == "Yes":
                    # Display success message and save the details
                    ExistingCompany.append(name)
                    ExistingCompanyAdd.append(Address)
                    ExistingCompany.remove("Other")
                    CompanyName = name
                else:
                    ExistingCompany.remove(name)
                    ExistingCompanyAdd.remove(Address)
                    CompanyName = "Other"
                Dict = {"Company Name": ExistingCompany, "Address": ExistingCompanyAdd}
                df = pd.DataFrame(Dict)
                df.to_csv("CompanyDetails.csv")
        index = ExistingCompany.index(CompanyName)
        try:
            CompanyAddress = ExistingCompanyAdd[index]
        except:
            CompanyAddress = "N/A"
    # Second Column: Date
    with col2:
        BankNames = st.selectbox("**Choose Account**", ["Union Bank of India", "State Bank of India"], key="dropdown2")
        BankDetailsDict = {"Union Bank of India": {"BankNames":"Union Bank of India", "Account Holder Name" : "Tilak Raj Singh", "Account No.": "202510100014648", "IFSC":"UBIN0820253"}
                        , "State Bank of India" : {"BankNames":"State Bank of India","Account Holder Name" : "Tilak Raj Singh", "Account No.": "39896679286", "IFSC":"SBIN0013217"}}
        BankDetails = BankDetailsDict[BankNames]
        Invoice_date = st.date_input("**Invoice Date**")

    # Third Column: Total Cab
    with col3:
        InvoiceNumber = st.number_input("**InvoiceNumber**", min_value=0, max_value=1000, step=1)
        total_cab = st.number_input("**Total Cab**", min_value=1, max_value=100, step=1)
        
    if 'items' not in st.session_state:
        st.session_state['items'] = []
    col1, col2 = st.columns([2, 2]) 

    with col1:
        with st.form(key='item_form'):
            # Customer Details
            Cab_Details = st.text_input("Cab Name and Number")
            Route_Details = st.text_input("Route Details")
        
            # Item Entry
            MonthlyPrice = st.number_input("Monthly Price", min_value=0, value=0)
            Start_date = st.date_input("**Start Date**")
            End_date = st.date_input("**End Date**")
            Additional_price = st.number_input("Additional Charges", min_value=0, value=0)
            # Submit button for adding an item
            submit_button = st.form_submit_button(label='Add New Item')
        
            # When the user submits the form to add the item, append the item to the list
            if submit_button:
                if Cab_Details and MonthlyPrice > 0 and Route_Details and End_date > Start_date:
                    # Add item to the session state list
                    TotalDays = (End_date - Start_date).days + 1
                    if  TotalDays == 30:
                        Cab_Monthly = MonthlyPrice
                    else:
                        Cab_Monthly = MonthlyPrice*(TotalDays/30)
                    st.session_state['items'].append({
                        'Cab name': Cab_Details,
                        'Route Details': Route_Details,
                        'Monthly Price': MonthlyPrice,
                        'Start Date' : Start_date,
                        'End Date': End_date,
                        'Additional Charge': Additional_price,
                        'Cab Monthly Charge': Cab_Monthly,
                        'Total Charge': Cab_Monthly + Additional_price
                    })
                    # Reset the form fields by simply not using st.experimental_rerun
                    # The next cycle will show the updated state without rerunning the script manually
                    st.write("Cab added! You can now add another CAB.")
                else:
                    st.error("Please enter valid Cab details."   ) 
    
    
    
    with col2:
        # Display selected options
        st.write("### Bill Summary")
        st.write(f"- Invoice Number: {InvoiceNumber}")
        st.write(f"- Bill to: {CompanyName}, Address: {CompanyAddress}")
        st.write(f"- Bank Details:")
        Col1 = list(BankDetails.keys())
        Col2 = list(BankDetails.values())
        Bankdf = pd.DataFrame({"Field":Col1, "Value":Col2})
        st.write(Bankdf)
        st.write(f"- Invoice Date: {Invoice_date}")
        st.write(f"- Total Cab: {total_cab}")
    
        # Display all added items
        if st.session_state['items']:
            st.subheader("Cab Details")
            total_amount = 0
            for i, item in enumerate(st.session_state['items']):
                st.write(f"{i+1}. {item['Cab name']} - Route Details: {item['Route Details']} - Monthly Price: ${item['Monthly Price']} - Start Date: ${item['Start Date']} - End Date: ${item['End Date']} - Cab Monthly Charge: ${item['Cab Monthly Charge']} - Additional Charge: ${item['Additional Charge']} - Total Charge: ${item['Total Charge']}")
                total_amount += item['Total Charge']
        
            st.write(f"**Total Amount: Rs{total_amount}**")

if __name__ == "__main__":
    main()
