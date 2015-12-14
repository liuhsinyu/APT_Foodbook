package com.foodbook.foodbook;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.provider.MediaStore;
import android.graphics.Bitmap;
import android.widget.ImageView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.content.Intent;
import java.io.ByteArrayOutputStream;

import com.beardedhen.androidbootstrap.BootstrapButton;

/**
 * Created by liuhsinyu on 15/12/13.
 */
public class CameraFragment extends Fragment {
    static final int REQUEST_IMAGE_CAPTURE = 1;
    View view;
    Context context;
    String mCurrentPhotoPath;
    Bitmap imageBitmap;
    String recipe_id;
    String recipe_name;

    public static CameraFragment newInstance(String recipe_id,String recipe_name) {
        CameraFragment myFragment = new CameraFragment();

        Bundle args = new Bundle();
        args.putString("recipe_id", recipe_id);
        args.putString("recipe_name",recipe_name);
        myFragment.setArguments(args);

        return myFragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.activity_camera, container, false);
        recipe_id = getArguments().getString("recipe_id");
        recipe_name = getArguments().getString("recipe_name");
        BootstrapButton takePictureButton = (BootstrapButton) view.findViewById(R.id.take_picture);
        takePictureButton.setOnClickListener(
                new View.OnClickListener(){
                    @Override
                    public void onClick(View v){
                        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
                            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
                        }
                    }
                }
        );

        return view;
    }


    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {

        if (requestCode == REQUEST_IMAGE_CAPTURE) {
            Bundle extras = data.getExtras();
            imageBitmap = (Bitmap) extras.get("data");
            ImageView imgView = (ImageView) view.findViewById(R.id.thumbnail);
            imgView.setImageBitmap(imageBitmap);


            BootstrapButton btn = (BootstrapButton) view.findViewById(R.id.use_picture);
            btn.setClickable(true);
            btn.setEnabled(true);
            btn.setOnClickListener(
                    new View.OnClickListener() {
                        @Override
                        public void onClick(View view) {
                            ByteArrayOutputStream stream = new ByteArrayOutputStream();
                            imageBitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
                            byte[] byteArray = stream.toByteArray();
                            ((MainActivity)getActivity()).displayIMadeItView(recipe_id,recipe_name,byteArray);
                        }
                    }
            );
        }
    }



}
