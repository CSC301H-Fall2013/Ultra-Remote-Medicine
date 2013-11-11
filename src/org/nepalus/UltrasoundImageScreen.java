package org.nepalus;

import java.io.File;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;

public class UltrasoundImageScreen extends Activity {
	static String IMAGE_DIRECTORY = "ultrasound";
	static String IMAGE_NAME="the_image";
	private static final int CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE = 100;

	Context mContext;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.ultrasoundimage);
        mContext = this;
    }
    

    @Override
	protected void onResume() {
		super.onResume();
        // create Intent to take a picture and return control to the calling application
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        Uri fileUri = getOutputMediaFileUri(); // create a file to save the image
        intent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri); // set the image file name

        // start the image capture Intent
        startActivityForResult(intent, CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE);
	}

	@Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == CAPTURE_IMAGE_ACTIVITY_REQUEST_CODE) {
            if (resultCode == RESULT_OK) {
                // Image captured and saved to fileUri specified in the Intent
            	Intent i = new Intent(this, MetadataScreen.class);
            	startActivity(i);
            } else if (resultCode == RESULT_CANCELED) {
            	//return to previous screen
            	onBackPressed();
            } else {
                //TODO Image capture failed, advise user
            }
        }
    }

	/** Create a file Uri for saving an image */
	public static Uri getOutputMediaFileUri(){
	      return Uri.fromFile(getOutputMediaFile());
	}
	
	/** Create a File for saving an image */
	private static File getOutputMediaFile(){

		String externalStorageState = Environment.getExternalStorageState();
		boolean isExternalStorageWriteable = Environment.MEDIA_MOUNTED.equals(externalStorageState);
		if (!isExternalStorageWriteable) {
		    //TODO inform user that no SD card available
			return null;
		}
		
	    File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
	              Environment.DIRECTORY_PICTURES), IMAGE_DIRECTORY);
	    // This location works best if you want the created images to be shared
	    // between applications and persist after the app has been uninstalled.

	    // Create the storage directory if it does not exist
	    if (! mediaStorageDir.exists()){
	        if (! mediaStorageDir.mkdirs()){
	            //TODO handle directory creation error
	            return null;
	        }
	    }

	    //TODO Create a unique media file name for each invocation
	    File mediaFile  = new File(mediaStorageDir.getPath() + File.separator +
	        IMAGE_NAME + ".jpg");

	    return mediaFile;
	}
}
