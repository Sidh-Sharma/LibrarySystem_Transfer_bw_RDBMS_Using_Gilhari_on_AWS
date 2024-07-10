package com.mycompany.gilhari5;

import org.json.JSONException;
import org.json.JSONObject;

import com.softwaretree.jdx.JDX_JSONObject;

public class LoanHist extends JDX_JSONObject {

    public LoanHist() {
        super();
    }

    public LoanHist(JSONObject jsonObject) throws JSONException {
        super(jsonObject);
    }
}