1. Renewal transaction.
For renewal transaction, send the master_policy_id that's due for renewal and the new expiry date
Parameters to pass include:
        - master_policy_id
        - transaction_type - RET
        - expiry_date
2. Endorsement
There are two options for endorsement,
----Endorse the master_policy by adding a new child_policy under it
    In this case, pass the following details:
            - master_policy_id
            - transaction_type - END
            - All child_policy policy details,such as,
            vehicle_details, 
            driver,
            modifications,
            benefits,
            extensions, 
            rate,
            customer_number,
            date_expiry,
            premium_amount,
            transaction_type,
            insurance_company,
            pricing_model

----Endorse the child_policy with a new benefit
    In this case a new benefit is appended to the child_policy,
    then the premium is recalculated.
        - Pass the following details:
            - child_policy_id (ID of the child policy that's to be updated with a new benefit)
            - transaction_type - END
            - benefits (contains any benefit(s) details that you've added)
            - premium_amount (new premium amount)

3. Extension
In this case a new extension is appended to a particular child_policy
Pass the following details:
        - child_policy_id (ID of the policy to be extended)
        - extensions (contains any extension(s) details)
        - transaction_type - EXT
        - premium_amount (new premium amount)

4. Refund
There are three options for refund:
----- When the item has been sold:
    In this case pass the following details:
        - refund_type - "sold"
        - transaction_type - "REF"
        - child_policy_id (id of the child_policy to be revised)
----- When the benefit has been cancelled:
    In this case pass the following details:
        - premium_amount (new premium_amount)
        - benefit_id, for the benefit(s) revised
        - refund_type - "benefit"
        - transaction_type - "REF"
        - child_policy_id (id of the child_policy to be revised)
----- When the sum_insured has been revised downwards
    In this case pass the following details
        - sum_insured (revised sum)
        - vehicle_id
        - refund_type - "sum_insured"
        - transaction_type - "REF"
        - child_policy_id (id of the child_policy to be revised)
        - premium_amount (new_premium_amount)


