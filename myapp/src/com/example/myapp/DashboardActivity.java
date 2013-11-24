package com.example.myapp;

import org.json.JSONObject;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class DashboardActivity extends Activity {
	Context mContext;
	private EditText mSearchKey;
	public static JSONObject jsonCheck;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dashboard);
        mContext = this;
        mSearchKey = (EditText) findViewById(R.id.search_box);
        TextView t = (TextView)findViewById(R.id.username_lb);
        t.setText("Welcome, " + MainActivity.jsonSessionId.optString("username"));
        
        Button newPatientButton = (Button) findViewById(R.id.add_new_patient_btn);
        newPatientButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
        		Intent i = new Intent(mContext, AddNewPatientActivity.class);
        		startActivity(i);
            }
        });
        
        Button newCaseButton = (Button) findViewById(R.id.add_new_case_btn);
        newCaseButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
        		Intent i = new Intent(mContext, AddNewCaseActivity.class);
        		startActivity(i);
            }
        });
        
        Button logoutButton = (Button) findViewById(R.id.logout_btn);
        logoutButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	SharedPreferences session_id = getSharedPreferences(MainActivity.SESSIONID, 0);
				SharedPreferences.Editor editor = session_id.edit();
				editor.putString("sessionid", null);
				editor.commit();
        		Intent i = new Intent(mContext, MainActivity.class);
        		startActivity(i);
            }
        });
        
        Button finishButton = (Button) findViewById(R.id.search_btn);
		finishButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/add_case";
							//Json package
							String jsonString = "{\"session_key\": \""
									+ MainActivity.jsonSessionId.optString("sessionid")
									+ "\", \"search_key\": \""
									+ mSearchKey.getText().toString()
									+ "\"}";
							
							jsonCheck = MainActivity.communicate(urlString, jsonString);
							
						} catch (Exception e) {
							e.printStackTrace();
						}
					}
				});
				thread.start();
				int timer = 0;
				while (jsonCheck == null && timer < 50) {
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					timer++;
				}
				Toast msg = Toast.makeText(getBaseContext(),
						(timer < 50 ? jsonCheck.optString("type")
								: "Server time out"), Toast.LENGTH_LONG);
				msg.show();
				msg = null;
				if (jsonCheck != null) {
					Intent i = new Intent(mContext, SearchResultActivity.class);
					startActivity(i);
				}
				jsonCheck = null;
			}
		});
    }
}
