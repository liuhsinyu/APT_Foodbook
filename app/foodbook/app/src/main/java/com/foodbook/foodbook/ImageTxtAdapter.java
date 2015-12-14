package com.foodbook.foodbook;

/**
 * Created by liuhsinyu on 15/12/12.
 */
import android.widget.BaseAdapter;
import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.GridView;
import android.widget.TextView;
import android.view.LayoutInflater;
import android.app.Activity;

import com.squareup.picasso.Picasso;

import org.w3c.dom.Text;

import java.util.ArrayList;

public class ImageTxtAdapter extends BaseAdapter {
    private Context mContext;
    private Activity mActivity;
    private ArrayList<String> ids;
    private ArrayList<String> imageURLs;
    private ArrayList<String> titles;
    private ArrayList<String> tags;
    private static LayoutInflater inflater=null;

    public ImageTxtAdapter(Context c, Activity a,ArrayList<String> ids,ArrayList<String> imageURLs,ArrayList<String> titles,ArrayList<String> tags) {
        mContext = c;
        mActivity = a;
        this.ids = ids;
        this.imageURLs = imageURLs;
        this.titles = titles;
        this.tags = tags;
        inflater = ( LayoutInflater )mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    public int getCount() {
        return imageURLs.size();
    }

    public Object getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    public class Holder
    {
        TextView tv1;
        TextView tv2;
        ImageView img;
    }
    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        // TODO Auto-generated method stub
        Holder holder=new Holder();
        View rowView;

        rowView = inflater.inflate(R.layout.activity_imgtxt, null);
        holder.tv1=(TextView) rowView.findViewById(R.id.textView1);
        holder.tv2=(TextView) rowView.findViewById(R.id.textView2);
        holder.img=(ImageView) rowView.findViewById(R.id.imageView1);
        holder.img.setScaleType(ImageView.ScaleType.CENTER_CROP);

        holder.tv1.setText(titles.get(position));
        holder.tv2.setText(tags.get(position));
        Picasso.with(mContext).load(imageURLs.get(position)).into(holder.img);
        holder.tv1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v){
                ((MainActivity)mActivity).displayRecipeView(ids.get(position));
            }
        });
        return rowView;
    }


}
