@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if not current_user.is_authenticated:
        flash("You isn't authenticated", category='danger')
        return redirect(url_for('login'))
    if current_user.roleId == 1:
        flash('You have no rules', category='danger')
        return redirect(url_for('index'))
    form = AddCompanyForm()
    if form.validate_on_submit():
        update_session(Company(name=form.name))
    return render_template('add_company.html', form=form, title='Добавление компании')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if not current_user.is_authenticated:
        flash("You isn't authenticated", category='danger')
        return redirect(url_for('login'))
    if current_user.roleId == 1:
        flash('You have no rules', category='danger')
        return redirect(url_for('index'))
    form = AddEmployeeForm()
    if form.validate_on_submit():
        login=form.login
        u = User.query.filter_by(login=login).first()
        if u is None:
            update_session(User(surname=form.surname, name=form.name,
                                patronomic=form.patronomic, login=login,
                                company_id=form.companyId, roleId=form.roleId))
            return redirect(url_for('add_employee'))
        flash('This ligin is used', category='danger')
        return redirect(url_for('add_employee'))
    return render_template('add_employee.html', form=form, title='Добавление сотрудника')