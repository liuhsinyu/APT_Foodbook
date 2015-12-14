package com.foodbook.foodbook;

import android.os.StrictMode;
import android.support.v4.app.Fragment;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.content.Intent;
import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.view.ViewGroup;
import android.net.Uri;
import android.widget.TextView;
import android.widget.Toast;


import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URLEncoder;
import java.net.URL;
import java.util.ArrayList;

import com.beardedhen.androidbootstrap.AwesomeTextView;
import com.beardedhen.androidbootstrap.BootstrapButton;
import com.beardedhen.androidbootstrap.BootstrapEditText;
import com.facebook.AccessToken;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;
import com.facebook.HttpMethod;
import com.facebook.login.LoginManager;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import com.facebook.login.LoginResult;
import com.facebook.login.widget.ProfilePictureView;
import com.facebook.share.widget.ShareButton;
import com.facebook.login.widget.LoginButton;
import com.facebook.share.model.SharePhotoContent;
import com.facebook.share.model.SharePhoto;
import com.facebook.share.widget.ShareDialog;
import com.facebook.CallbackManager;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.apache.http.Header;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.Arrays;

/**
 * Created by liuhsinyu on 15/12/13.
 */
public class IMadeItFragment extends Fragment{
    CallbackManager callbackManager;
    ShareDialog shareDialog;
    private static final int PICK_IMAGE = 1;
    private static final int CAMERA_IMAGE = 2;
    ShareButton shareButton;
    final ArrayList<String> user_id = new ArrayList<String>();
    View view;
    Context context;
    String recipe_id;
    String recipe_name;

    public static IMadeItFragment newInstance(String recipe_id,String recipe_name) {
        IMadeItFragment myFragment = new IMadeItFragment();

        Bundle args = new Bundle();
        args.putString("recipe_id", recipe_id);
        args.putString("recipe_name", recipe_name);
        myFragment.setArguments(args);

        return myFragment;
    }

    public static IMadeItFragment newInstance(String recipe_id,String recipe_name,byte[] byteArray) {
        IMadeItFragment myFragment = new IMadeItFragment();

        Bundle args = new Bundle();
        args.putString("recipe_id", recipe_id);
        args.putString("recipe_name", recipe_name);
        args.putByteArray("image", byteArray);
        myFragment.setArguments(args);

        return myFragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        FacebookSdk.sdkInitialize(container.getContext());
        LoginManager.getInstance().logInWithPublishPermissions(this, Arrays.asList("publish_actions"));

        view = inflater.inflate(R.layout.activity_imadeit, container, false);
        callbackManager = CallbackManager.Factory.create();
        recipe_id = getArguments().getString("recipe_id");
        recipe_name = getArguments().getString("recipe_name");
        final byte[] byteArray = getArguments().getByteArray("image");
        AwesomeTextView recipe_name_view = (AwesomeTextView) view.findViewById(R.id.recipe_name);

        recipe_name_view.setText(recipe_name);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        GraphRequest request = new GraphRequest(
                AccessToken.getCurrentAccessToken(),
                "/me",
                null,
                HttpMethod.GET,
                new GraphRequest.Callback() {
                    public void onCompleted(GraphResponse response) {
                        try {
                            System.out.println(response.toString());
                            JSONObject obj = response.getJSONObject();
                            user_id.clear();
                            user_id.add(obj.getString("id"));
                        } catch(JSONException ex) {
                            ex.printStackTrace();
                        }
                    }
                }
        );
        request.executeAndWait();
        shareButton = (ShareButton)view.findViewById(R.id.fb_share_button);

        if(byteArray!=null) {
            final Bitmap bitmapImage = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
            if (bitmapImage != null) {
                ImageView imgView = (ImageView) view.findViewById(R.id.thumbnail);
                imgView.setImageBitmap(bitmapImage);

                BootstrapButton uploadButton = (BootstrapButton) view.findViewById(R.id.upload_to_server);
                uploadButton.setClickable(true);
                uploadButton.setEnabled(true);


                shareButton.setEnabled(true);
                shareButton.setClickable(true);
                shareButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        SharePhoto photo = new SharePhoto.Builder()
                                .setBitmap(bitmapImage)
                                .build();

                        SharePhotoContent content = new SharePhotoContent.Builder()
                                .addPhoto(photo)
                                .build();

                        shareButton.setShareContent(content);
                    }
                });



                uploadButton.setOnClickListener(
                        new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {

                                // Get photo caption

                                BootstrapEditText text = (BootstrapEditText) view.findViewById(R.id.upload_message);
                                String comments = text.getText().toString();

                                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                                bitmapImage.compress(Bitmap.CompressFormat.JPEG, 50, baos);
                                byte[] b = baos.toByteArray();

                                getUploadURL(b, comments);

                            }
                        }
                );
            }
        }

        BootstrapButton chooseFromLibraryButton = (BootstrapButton) view.findViewById(R.id.choose_from_library);
        chooseFromLibraryButton.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {

                        // To do this, go to AndroidManifest.xml to add permission
                        Intent galleryIntent = new Intent(Intent.ACTION_PICK,
                                android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                        // Start the Intent
                        startActivityForResult(galleryIntent, PICK_IMAGE);
                    }
                }
        );

        BootstrapButton usecameraButton = (BootstrapButton) view.findViewById(R.id.use_camera);
        usecameraButton.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        ((MainActivity) getActivity()).displayCameraView(recipe_id, recipe_name);
                    }
                }
        );
        context = container.getContext();
        return view;
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_IMAGE && data != null && data.getData() != null) {
            Uri selectedImage = data.getData();

            // User had pick an image.

            String[] filePathColumn = {MediaStore.Images.ImageColumns.DATA};
            Cursor cursor = context.getContentResolver().query(selectedImage, filePathColumn, null, null, null);
            cursor.moveToFirst();

            // Link to the image

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String imageFilePath = cursor.getString(columnIndex);
            cursor.close();

            // Bitmap imaged created and show thumbnail

            ImageView imgView = (ImageView) view.findViewById(R.id.thumbnail);
            final Bitmap bitmapImage = BitmapFactory.decodeFile(imageFilePath);
            imgView.setImageBitmap(bitmapImage);

            // Enable the upload button once image has been uploaded

            BootstrapButton uploadButton = (BootstrapButton) view.findViewById(R.id.upload_to_server);
            uploadButton.setClickable(true);
            uploadButton.setEnabled(true);

            ShareButton shareButton = (ShareButton)view.findViewById(R.id.fb_share_button);
            shareButton.setEnabled(true);
            shareButton.setClickable(true);
            SharePhoto photo = new SharePhoto.Builder()
                    .setBitmap(bitmapImage)
                    .build();
            SharePhotoContent content = new SharePhotoContent.Builder()
                    .addPhoto(photo)
                    .build();
            shareButton.setShareContent(content);

            uploadButton.setOnClickListener(
                    new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {

                            // Get photo caption

                            BootstrapEditText text = (BootstrapEditText) view.findViewById(R.id.upload_message);
                            String comments = text.getText().toString();

                            ByteArrayOutputStream baos = new ByteArrayOutputStream();
                            bitmapImage.compress(Bitmap.CompressFormat.JPEG, 50, baos);
                            byte[] b = baos.toByteArray();
                            System.out.println("HIHIHIHIHI");
                            getUploadURL(b, comments);

                        }
                    }
            );
        }else {
            callbackManager.onActivityResult(requestCode, resultCode, data);
        }
    }

    private void getUploadURL(final byte[] encodedImage, final String comments){
        String request_url = "http://foodbook-1150.appspot.com/uploadHandler";
        System.out.println(request_url);
        String upload_url;
        try {
            URL obj = new URL(request_url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            // optional default is GET
            con.setRequestMethod("GET");

            int responseCode = con.getResponseCode();

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            System.out.println(response.toString());
            JSONObject jObject = new JSONObject(response.toString());
            upload_url = jObject.getString("upload_url");
            postToServer(encodedImage,comments,upload_url);
        }catch (Exception e){

        }
    }

    private void postToServer(byte[] encodedImage,String comments, String upload_url){
        System.out.println("URL");
        System.out.println(upload_url);
        System.out.println(recipe_id);
        System.out.println(comments);
        System.out.println(user_id.get(0));

        RequestParams params = new RequestParams();
        params.put("file", new ByteArrayInputStream(encodedImage));
        params.put("user_id", user_id.get(0));
        params.put("recipe_id",recipe_id);
        params.put("author_comments",comments);

        AsyncHttpClient client = new AsyncHttpClient();
        client.post(upload_url, params, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] response) {
                Toast.makeText(context, "Upload Successful", Toast.LENGTH_SHORT).show();
                ((MainActivity)getActivity()).displayRecipeView(recipe_id);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] errorResponse, Throwable e) {
                System.out.println(e.toString());
            }

        });



    }

}
