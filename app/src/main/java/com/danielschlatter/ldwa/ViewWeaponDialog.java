package com.danielschlatter.ldwa;

import android.app.AlertDialog;
import android.app.Dialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.DialogFragment;

public class ViewWeaponDialog extends DialogFragment {
    private Weapon weapon;
    public ViewWeaponDialog() {}
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        Dialog dialog = super.onCreateDialog(savedInstanceState);
        dialog.setCanceledOnTouchOutside(true);
        LayoutInflater inflater = requireActivity().getLayoutInflater();
        View title = inflater.inflate(R.layout.title_bar, null);
        TextView name = title.findViewById(R.id.name);
        name.setText(weapon.getName());
        TextView type = title.findViewById(R.id.type);
        TextView archetype = title.findViewById(R.id.archetype);
        ImageView icon = title.findViewById(R.id.icon);
        ImageView ammo_icon = title.findViewById(R.id.ammo);
        ImageView element_icon = title.findViewById(R.id.element);
        type.setText(weapon.getType());
        archetype.setText(weapon.getArchetype());
        icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getIcon(), "mipmap", this.requireContext().getPackageName()));
        element_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getElement_icon(), "mipmap", this.requireContext().getPackageName()));
        ammo_icon.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getAmmo_icon(), "mipmap", this.requireContext().getPackageName()));
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity()).setCustomTitle(title);

        View dialogView = inflater.inflate(R.layout.dialog_view_weapon, null);
        ImageView screenshot = dialogView.findViewById(R.id.imageViewScreenshot);
        TextView synergyTextView = dialogView.findViewById(R.id.textViewSynergy);
        TextView perk_column_1TextView = dialogView.findViewById(R.id.textViewPerk_column_1);
        TextView perk_column_2TextView = dialogView.findViewById(R.id.textViewPerk_column_2);
        TextView perk_column_3TextView = dialogView.findViewById(R.id.textViewPerk_column_3);
        TextView perk_column_4TextView = dialogView.findViewById(R.id.textViewPerk_column_4);

        Button buttonClose = dialogView.findViewById(R.id.buttonClose);

        synergyTextView.setText(weapon.getSynergy());
        perk_column_1TextView.setText(weapon.getPerk_column_1());
        perk_column_2TextView.setText(weapon.getPerk_column_2());
        perk_column_3TextView.setText(weapon.getPerk_column_3());
        perk_column_4TextView.setText(weapon.getPerk_column_4());
        screenshot.setImageResource(this.requireContext().getResources().getIdentifier(weapon.getScreenshot(), "drawable", this.requireContext().getPackageName()));

        builder.setView(dialogView).setMessage(" ");
        buttonClose.setOnClickListener(view -> dismiss());
        return builder.create();
    }

    public void sendSelectedWeapon (Weapon weapon) {
        this.weapon = weapon;
    }
}
