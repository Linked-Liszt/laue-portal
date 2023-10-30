export default function FieldCkbx({label}) {
    return (
        <div className="form-control">
            <label className="label cursor-pointer space-x-2">
                <span className="label-text text-lg">{label}</span>
                <input type="checkbox" className="checkbox checkbox-primary" />
            </label>
        </div>
    )
}