package com.example.myapp;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;

public class PatientPageActivity extends Activity {
	Context mContext;

	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_page);
        mContext = this;

        //patientpage_add_new_case_btn
        //patientpage_pre_btn
        //patientpage_next_btn

    }
}