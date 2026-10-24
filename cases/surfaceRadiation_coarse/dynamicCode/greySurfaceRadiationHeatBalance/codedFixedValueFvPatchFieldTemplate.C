/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "codedFixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "read.H"

//{{{ begin codeInclude

//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = a5a70ea331d2a8420d21030acaaa7987c447865f
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void greySurfaceRadiationHeatBalance_a5a70ea331d2a8420d21030acaaa7987c447865f(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchScalarField,
    greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField
);


const char* const greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::SHA1sum =
    "a5a70ea331d2a8420d21030acaaa7987c447865f";


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::
greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField
(
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF,
    const dictionary& dict
)
:
    fixedValueFvPatchField<scalar>(p, iF, dict)
{
    if (false)
    {
        Info<<"construct greySurfaceRadiationHeatBalance sha1: a5a70ea331d2a8420d21030acaaa7987c447865f"
            " from patch/dictionary\n";
    }
}


greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::
greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField
(
    const greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField& ptf,
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF,
    const fieldMapper& mapper
)
:
    fixedValueFvPatchField<scalar>(ptf, p, iF, mapper)
{
    if (false)
    {
        Info<<"construct greySurfaceRadiationHeatBalance sha1: a5a70ea331d2a8420d21030acaaa7987c447865f"
            " from patch/DimensionedField/mapper\n";
    }
}


greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::
greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField
(
    const greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField& ptf,
    const DimensionedField<scalar, volMesh>& iF
)
:
    fixedValueFvPatchField<scalar>(ptf, iF)
{
    if (false)
    {
        Info<<"construct greySurfaceRadiationHeatBalance sha1: a5a70ea331d2a8420d21030acaaa7987c447865f "
            "as copy/DimensionedField\n";
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::
~greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField()
{
    if (false)
    {
        Info<<"destroy greySurfaceRadiationHeatBalance sha1: a5a70ea331d2a8420d21030acaaa7987c447865f\n";
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void greySurfaceRadiationHeatBalanceFixedValueFvPatchScalarField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        Info<<"updateCoeffs greySurfaceRadiationHeatBalance sha1: a5a70ea331d2a8420d21030acaaa7987c447865f\n";
    }

//{{{ begin code
    #line 16 "/home/jerlin/Documents/projects/blt/cases/surfaceRadiation_coarse/0/T/plate"

         const scalar sigma = 5.670374419e-8;
         const scalar emissivity = 0.8;
         const scalar Tsur = 300.0;
         const scalar qHeater = 1000.0;
         const scalar kappa = 0.02613;
         const scalarField ti(this->patchInternalField());
         const scalarField dc(this->patch().deltaCoeffs());
         scalarField tw(ti.size());
         forAll(ti, facei)
         {
             scalar t = max(ti[facei] + qHeater/(kappa*dc[facei]), scalar(1));
             for (label iter=0; iter<12; ++iter)
             {
                 const scalar t4 = sqr(sqr(t));
                 const scalar f = kappa*dc[facei]*(t - ti[facei])
                     + emissivity*sigma*(t4 - sqr(sqr(Tsur))) - qHeater;
                 const scalar df = kappa*dc[facei] + 4*emissivity*sigma*t*t*t;
                 t = max(t - f/df, scalar(1));
             }
             tw[facei] = t;
         }
         operator==(tw);
     
//}}} end code

    this->fixedValueFvPatchField<scalar>::updateCoeffs();
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

