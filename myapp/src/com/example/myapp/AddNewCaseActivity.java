package com.example.myapp;

import java.io.ByteArrayOutputStream;

import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class AddNewCaseActivity extends ActivityAPI {
	Context mContext;
	private EditText mPatientID;
	private EditText mPatientPriority;
	private EditText mPatientComments;
	public static JSONObject jsonCheck;
	public static JSONObject jsonCheck2;
	public static String photo;
	
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.add_new_case);
	    mContext = this;
        mPatientID = (EditText) findViewById(R.id.patient_id);
        mPatientPriority = (EditText) findViewById(R.id.patient_priority);
        mPatientComments = (EditText) findViewById(R.id.patient_comments);
        
		Resources r = this.getResources();
        Bitmap bm = BitmapFactory.decodeResource(r, R.drawable.ideal_image);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();  
        bm.compress(Bitmap.CompressFormat.JPEG, 100, baos); //bm is the bitmap object   
        byte[] b = baos.toByteArray(); 
        photo = Base64.encodeToString(b, Base64.DEFAULT);
        
        
        Button finishButton = (Button) findViewById(R.id.add_case_finish);
		finishButton.setOnClickListener(new View.OnClickListener() {
			public void onClick(View view) {
				Thread thread = new Thread(new Runnable() {
					@Override
					public void run() {
						try {
							// URL
							String urlString = "http://ultra-remote-medicine."
									+ "herokuapp.com/mobile/add_case";
							//String urlString = "http://10.0.2.2:8000/mobile/add_case";
							//Json package
							String jsonString = "{\"session_key\": \""
									+ jsonSessionId.optString("sessionid")
									+ "\", \"patient\": \""
									+ mPatientID.getText().toString()
									+ "\", \"comments\": \""
									+ mPatientComments.getText().toString()
									+ "\", \"priority\": \""
									+ mPatientPriority.getText().toString()
									+ "\"}";
							
							jsonCheck = communicate(urlString, jsonString);
							
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
					jsonCheck2=null;
					Thread threadpic = new Thread(new Runnable() {
						@Override
						public void run() {
							try {
								// URL
								String urlString = "http://ultra-remote-medicine."
										+ "herokuapp.com/mobile/upload";
								//String urlString = "http://10.0.2.2:8000/mobile/upload";
								//Json package
								String jsonString = "{\"session_key\": \""
										+ jsonSessionId.optString("sessionid")
										+ "\", \"case_id\": \""
										+ jsonCheck.optString("case_id")
										+ "\", \"image_string\": \""
										+ photo
										+ "\"}";
								
								jsonCheck2 = communicate(urlString, jsonString);
								
							} catch (Exception e) {
								e.printStackTrace();
							}
						}
					});
					threadpic.start();
					int timer2 = 0;
					while (jsonCheck2 == null && timer2 < 50) {
						try {
							Thread.sleep(200);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}
						timer2++;
					}
					msg = Toast.makeText(getBaseContext(),
							(timer2 < 50 ? jsonCheck2.optString("type")
									: "Server time out"), Toast.LENGTH_LONG);
					msg.show();
					msg = null;
					if (jsonCheck2 != null) {
						
						
						
						
						
						Intent i = new Intent(mContext, SearchResultActivity.class);
						startActivity(i);
					}
					
					jsonCheck2 = null;
				
					
					
					
					
					//Intent i = new Intent(mContext, SearchResultActivity.class);
					//startActivity(i);
				}
				jsonCheck = null;
			}
		});
	}
}
