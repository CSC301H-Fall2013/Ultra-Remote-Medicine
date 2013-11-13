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

public class AddNewPatientScreen extends Activity {
	private Activity mActivity;
	private EditText mPatientID;
	private EditText mPatientPriority;
	private EditText mPatientComments;
	
    private NepalUltrasoundAPI api = new NepalUltrasoundSender();
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.metadata);
        
        mActivity = this;
        mPatientID = (EditText) findViewById(R.id.patient_id);
        mPatientPriority = (EditText) findViewById(R.id.patient_priority);
        mPatientComments = (EditText) findViewById(R.id.patient_comments);
        		
        ImageView thumbnail = (ImageView) findViewById(R.id.ultrasound_case_thumbnail);
        thumbnail.setImageURI(UltrasoundImageScreen.getOutputMediaFileUri());
        
        Button nextButton = (Button) findViewById(R.id.casefinish);
        nextButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
            	submit();
                Toast.makeText(mActivity, getString(R.string.image_success), Toast.LENGTH_LONG).show();
                mActivity.moveTaskToBack(true);
            }
        });
    }
    
    private void submit(){    	    	
    	final String patientID = mPatientID.getText().toString();    	
    	final String patientPriority = mPatientPriority.getText().toString(); 
    	final String patientComments = mPatientComments.getText().toString(); 
    	
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
						HttpResponse response = api.sendcase(patientID, 
								patientPriority, patientComments, photo);
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
