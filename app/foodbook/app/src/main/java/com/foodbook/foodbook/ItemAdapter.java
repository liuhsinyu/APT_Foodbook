package com.foodbook.foodbook;

import java.util.List;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;

public class ItemAdapter extends BaseAdapter {

    private ArrayList<Product> mProductList;
    private static LayoutInflater mInflater=null;
    private Context mContext;
    private boolean mShowCheckbox;

    public ItemAdapter(Context c, ArrayList<Product> list) {
        mProductList = list;
        mContext = c;
        mShowCheckbox = true;
        mInflater = ( LayoutInflater )mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public int getCount() {
        return mProductList.size();
    }

    @Override
    public Object getItem(int position) {
        return mProductList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ViewItem item=new ViewItem();
        View rowView;

        rowView = mInflater.inflate(R.layout.activity_item, null);
        item.productTitle=(TextView) rowView.findViewById(R.id.TextViewItem);
        item.productCheckbox=(CheckBox) rowView.findViewById(R.id.CheckBoxSelected);

        item.productTitle.setText(mProductList.get(position).title);
        item.productCheckbox.setChecked(mProductList.get(position).selected);

        return rowView;
    }


    private class ViewItem {
        TextView productTitle;
        CheckBox productCheckbox;
    }
}

