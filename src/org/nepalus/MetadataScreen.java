package org.nepalus;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

public class MetadataScreen extends Activity {
	private Activity mActivity;
	private EditText mPatientFirstName;
	private EditText mPatientLastName;
	private EditText mPatientSex;
	private EditText mPatientDOB;
	private EditText mPatientHealthID;
	private EditText mPatientGPSCoordinates;
	private EditText mPatientAddress;
	private EditText mPatientPhoneNumber;
	private EditText mPatientEmail;
	
    private NepalUltrasoundAPI api = new NepalUltrasoundSender();
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.metadata);
        
        mActivity = this;
        mPatientFirstName = (EditText) findViewById(R.id.patient_first_name);
        mPatientLastName = (EditText) findViewById(R.id.patient_last_name);
        mPatientSex = (EditText) findViewById(R.id.patient_sex);
        mPatientDOB = (EditText) findViewById(R.id.patient_dob);
        mPatientHealthID = (EditText) findViewById(R.id.patient_health_id);
        mPatientGPSCoordinates = (EditText) findViewById(R.id.patient_gps_coordinates);
        mPatientAddress = (EditText) findViewById(R.id.patient_address);
        mPatientPhoneNumber = (EditText) findViewById(R.id.patient_phone_number);
        mPatientEmail = (EditText) findViewById(R.id.patient_email);
        		
        ImageView thumbnail = (ImageView) findViewById(R.id.ultrasound_thumbnail);
        thumbnail.setImageURI(UltrasoundImageScreen.getOutputMediaFileUri());
        
        Button nextButton = (Button) findViewById(R.id.finish);
        nextButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	submit();
                Toast.makeText(mActivity, getString(R.string.image_success), Toast.LENGTH_LONG).show();
                mActivity.moveTaskToBack(true);
            }
        });
    }
    
    private void submit(){    	    	
    	final String patientFirstName = mPatientFirstName.getText().toString();    	
    	final String patientLastName = mPatientLastName.getText().toString();
    	final String patientSex = mPatientSex.getText().toString();
    	final String patientDOB = mPatientDOB.getText().toString();
    	final String patientHealthID = mPatientHealthID.getText().toString();
    	final String patientGPSCoordinates = mPatientGPSCoordinates.getText().toString();
    	final String patientAddress = mPatientAddress.getText().toString();
    	final String patientPhoneNumber = mPatientPhoneNumber.getText().toString();
    	final String patientEmail = mPatientEmail.getText().toString();
    	
    	
    	BitmapFactory.Options bitmapOptions = new BitmapFactory.Options();
    	final Bitmap photo;
    	
    	bitmapOptions.outMimeType = "image/png";
    	
    	try {
	        URL aURL = new URL(UltrasoundImageScreen.getOutputMediaFileUri().toString());
	        URLConnection conn = aURL.openConnection();
	        conn.connect();
	        InputStream is = conn.getInputStream();
	        BufferedInputStream bis = new BufferedInputStream(is);
	        photo = BitmapFactory.decodeStream(bis);
	        bis.close();
	        is.close();

	        new Thread(new Runnable() {
	            public void run() {
	            	try {
	            		api.setURL("http://192.168.100.245:3000/send");
						HttpResponse response = api.send(patientFirstName, 
								patientLastName, patientSex, patientDOB,
								patientHealthID, patientGPSCoordinates, patientAddress,
								patientPhoneNumber, patientEmail, photo);
						Log.d("API", "sent");											
					} catch (ClientProtocolException e) {
						Log.d("API", e.getMessage());						
					} catch (IOException e) {
						Log.d("API", e.getMessage());
					}    
	            }
	          }).start();   
    	}
    	catch (IOException e) {
    		Log.d("loadBitmap", e.getMessage());
    	}
    	
    }
}
