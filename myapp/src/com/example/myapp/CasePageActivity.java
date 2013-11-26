package com.example.myapp;

import android.content.Context;
import android.os.Bundle;

public class CasePageActivity extends ActivityAPI {
	Context mContext;

	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.case_page);
        mContext = this;


    }
}
