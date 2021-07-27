package com.danielschlatter.ldwa;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class WeaponAdapter extends RecyclerView.Adapter<WeaponAdapter.ListItemHolder> {
    private MainActivity mainActivity;
    private ArrayList<Weapon> weaponList;

    public WeaponAdapter (MainActivity mainActivity, ArrayList<Weapon> weaponList) {
        this.mainActivity = mainActivity;
        this.weaponList = weaponList;

    }

    @NonNull
    @Override
    public ListItemHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View listItem = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.list_item, parent, false);

        return new ListItemHolder(listItem);
    }

    @Override
    public void onBindViewHolder(@NonNull ListItemHolder holder, int position) {
        Weapon weapon = weaponList.get(position);
        holder.textViewName.setText(weapon.getName());
        holder.icon.setImageResource(mainActivity.getResources().getIdentifier(weapon.getIcon(), "mipmap", mainActivity.getPackageName()));

    }

    @Override
    public int getItemCount() {
        return weaponList.size();
    }

    public class ListItemHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        private final TextView textViewName;
        private final ImageView icon;
        public ListItemHolder (View view) {
            super(view);
            icon = view.findViewById(R.id.imageViewIcon);
            textViewName = view.findViewById(R.id.textViewName);
            view.setClickable(true);
            view.setOnClickListener(this);
        }

        public void onClick (View view) {

            mainActivity.showWeapon(getAdapterPosition());
        }

    }
}
